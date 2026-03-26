import concurrent.futures
import json
import math
import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

from utils import find_file, strip_prefix


def slice_coco_dataset(
    input_dir: Path,
    output_dir: Path,
    slice_size: Tuple[int, int] = (640, 640),
    overlap_ratio: Tuple[float, float] = (0.2, 0.2),
    jobs: int = 4,
    nas_path: Optional[Path] = None,
    nas_prefix: str = "",
):
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory not found: {input_dir}")

    output_dir = output_dir.resolve()
    img_dir = output_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    json_files = sorted(list(input_dir.rglob("*.json")))
    if not json_files:
        raise FileNotFoundError(f"No COCO JSON annotation file found in: {input_dir}")

    if nas_path:
        # Fill images from NAS for all JSONs upfront (if needed)
        for json_file in json_files:
            _fill_coco_images_from_nas(json_file, input_dir, nas_path, nas_prefix)

    # If there's exactly one JSON and we have multiple jobs, process it in parallel chunks
    main_json = json_files[0]
    if len(json_files) == 1:
        if jobs > 1:
            with open(main_json, "r") as f:
                full_data = json.load(f)

            images = full_data.get("images", [])
            if not images:
                return

            chunks = _split_coco_json(full_data, jobs)
            chunk_dir = Path(tempfile.mkdtemp(prefix="coco_chunks_"))
            chunk_paths, sliced_json_paths = [], []

            for i, chunk_data in enumerate(chunks):
                chunk_file = chunk_dir / f"chunk_{i:03d}.json"
                with open(chunk_file, "w") as f:
                    json.dump(chunk_data, f)
                chunk_paths.append(chunk_file)

            src_image_dir = _resolve_image_dir(input_dir, main_json)

            with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as executor:
                futures = [
                    executor.submit(
                        _slice_coco_chunk,
                        chunk_path,
                        src_image_dir,
                        output_dir,
                        slice_size,
                        overlap_ratio,
                    )
                    for chunk_path in chunk_paths
                ]
                for future in concurrent.futures.as_completed(futures):
                    sliced_json_paths.append(future.result())

            _merge_coco_jsons(
                sliced_json_paths,
                output_dir / "annotations" / main_json.name,
            )

            for p in sliced_json_paths:
                p.unlink(missing_ok=True)
            shutil.rmtree(chunk_dir, ignore_errors=True)
            return

    # Single file or multiple files (non-parallel/serial)
    all_sliced_jsons = []
    for json_file in json_files:
        src_image_dir = _resolve_image_dir(input_dir, json_file)
        sliced_json = _slice_coco_chunk(
            json_file, src_image_dir, output_dir, slice_size, overlap_ratio
        )
        all_sliced_jsons.append(sliced_json)

    # If it was a single file, move the result to annotations/
    if len(json_files) == 1:
        target_json = output_dir / "annotations" / main_json.name
        target_json.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(all_sliced_jsons[0], target_json)
    else:
        print("Sliced multiple COCO files. Results are in images/ as *_coco.json")


def _split_coco_json(full_data: dict, num_chunks: int) -> List[dict]:
    """
    Splits a COCO dataset into `num_chunks` subsets, distributing images
    and their annotations evenly.
    """
    images = full_data.get("images", [])
    annotations = full_data.get("annotations", [])
    categories = full_data.get("categories", [])

    # Group annotations by image_id
    ann_by_img = {}
    for ann in annotations:
        ann_by_img.setdefault(ann["image_id"], []).append(ann)

    # Split images into chunks
    chunk_size = math.ceil(len(images) / num_chunks)
    chunks = []
    for i in range(0, len(images), chunk_size):
        chunk_images = images[i : i + chunk_size]
        img_ids = {img["id"] for img in chunk_images}
        chunk_anns = []
        for img_id in img_ids:
            chunk_anns.extend(ann_by_img.get(img_id, []))
        chunks.append(
            {
                "images": chunk_images,
                "annotations": chunk_anns,
                "categories": categories,
            }
        )
    return chunks


def _slice_coco_chunk(
    chunk_path: Path,
    image_dir: Path,
    output_dir: Path,
    slice_size: Tuple[int, int],
    overlap_ratio: Tuple[float, float],
) -> Path:
    """
    Worker that runs SAHI slice_coco on a single chunk JSON.
    The sliced JSON is placed directly in `output_dir` with the same name as `chunk_path`.
    """
    from sahi.slicing import slice_coco

    out_dir = Path(output_dir).resolve()
    img_out_dir = out_dir / "images"
    img_out_dir.mkdir(parents=True, exist_ok=True)

    output_name = chunk_path.stem
    slice_coco(
        coco_annotation_file_path=str(chunk_path),
        image_dir=str(image_dir),
        output_coco_annotation_file_name=output_name,
        output_dir=str(img_out_dir),
        slice_height=slice_size[0],
        slice_width=slice_size[1],
        overlap_height_ratio=overlap_ratio[0],
        overlap_width_ratio=overlap_ratio[1],
        verbose=0,
    )
    return img_out_dir / f"{output_name}_coco.json"


def _merge_coco_jsons(chunk_paths: List[Path], output_path: Path) -> None:
    """
    Merges multiple sliced COCO JSONs into one, reassigning image and annotation IDs
    to avoid conflicts. The categories are taken from the first chunk.
    """
    all_images = []
    all_annotations = []
    categories = None

    # Temporary ID mapping: old -> new
    next_image_id = 1
    next_ann_id = 1

    for chunk_path in chunk_paths:
        if not chunk_path.exists():
            continue

        with open(chunk_path, "r") as f:
            data = json.load(f)

        if categories is None:
            categories = data.get("categories", [])

        img_id_map = {}
        for img in data.get("images", []):
            old_id = img.get("id")
            new_id = next_image_id
            next_image_id += 1
            img_id_map[old_id] = new_id
            img["id"] = new_id
            all_images.append(img)

        for ann in data.get("annotations", []):
            old_img_id = ann.get("image_id")
            if old_img_id in img_id_map:
                ann["image_id"] = img_id_map[old_img_id]
                ann["id"] = next_ann_id
                next_ann_id += 1
                all_annotations.append(ann)

    merged = {
        "images": all_images,
        "annotations": all_annotations,
        "categories": categories,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(merged, f)


def _resolve_image_dir(extract_path: Path, coco_path: Path) -> Path:
    """
    Finds the root directory for images referenced in a COCO JSON.
    """
    with open(coco_path, "r") as f:
        data = json.load(f)

    if not data.get("images"):
        return extract_path

    # Take the first image path from JSON to find its location on disk
    sample_rel_path = data["images"][0]["file_name"]
    sample_filename = Path(sample_rel_path).name

    # Search for this filename in the extracted directory
    for p in extract_path.rglob(sample_filename):
        # Check if the suffix of the found path matches the relative path in JSON
        # e.g. if JSON says 'train/a.jpg' and we found '/tmp/images/train/a.jpg'
        # the base is '/tmp/images'
        found_path_str = str(p.absolute()).replace("\\", "/")
        rel_path_str = sample_rel_path.replace("\\", "/")

        if found_path_str.endswith(rel_path_str):
            # Calculate base path
            base_str = found_path_str[: -len(rel_path_str)].rstrip("/\\")
            base_path = Path(base_str)
            if base_path.exists():
                return base_path

    # Fallback candidates
    for cand in [extract_path / "images", extract_path]:
        if cand.exists():
            return cand

    return extract_path


def coco_to_yolo(input_dir: Path, output_dir: Path):
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory not found: {input_dir}")
    from datumaro.components.dataset import Dataset

    dataset = Dataset.import_from(str(input_dir), format="coco")
    dataset.export(str(output_dir), format="yolo", save_media=True)


def yolo_to_coco(
    input_dir: Path,
    output_dir: Path,
    nas_path: Optional[Path] = None,
    nas_prefix: str = "",
):
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory not found: {input_dir}")

    if nas_path:
        _fill_images_from_nas(input_dir, nas_path, nas_prefix)
    from datumaro.components.dataset import Dataset

    dataset = Dataset.import_from(str(input_dir), format="yolo")
    dataset.export(str(output_dir), format="coco_instances", save_media=True)


def _fill_images_from_nas(extract_path: Path, nas_path: Path, nas_prefix: str):
    """Locates and copies missing images from NAS based on label filenames."""
    image_exts = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
    search_dir = extract_path / "obj_train_data"
    if not search_dir.exists():
        search_dir = extract_path

    label_files = list(search_dir.rglob("*.txt"))

    for lbl in label_files:
        if lbl.name in ["classes.txt", "obj.names"]:
            continue

        if any(lbl.with_suffix(ext).exists() for ext in image_exts):
            continue

        rel_p = str(lbl.relative_to(search_dir))
        if nas_prefix and rel_p.startswith(nas_prefix):
            rel_p = rel_p[len(nas_prefix) :].lstrip("/")

        for ext in image_exts:
            nas_img = nas_path / Path(rel_p).with_suffix(ext)
            if nas_img.exists():
                shutil.copy2(nas_img, lbl.with_suffix(ext))
                break


def _fill_coco_images_from_nas(
    coco_path: Path, extract_path: Path, nas_path: Path, nas_prefix: str
):
    """Locates and symlinks missing COCO images from NAS into extraction directory."""
    with open(coco_path, "r") as f:
        data = json.load(f)

    for img in data.get("images", []):
        file_name = img["file_name"]
        local_path = extract_path / file_name
        if local_path.exists():
            continue

        clean_rel_p = strip_prefix(file_name, nas_prefix)
        nas_img = nas_path / clean_rel_p

        if nas_img.exists():
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.symlink_to(nas_img)


def filter_coco_unannotated(input_dir: Path, output_dir: Path):
    """Removes images that do not have any annotations from a COCO dataset."""
    coco_json = find_file(input_dir, ["*.json"])
    if not coco_json:
        raise FileNotFoundError(f"No COCO JSON found in {input_dir}")

    with open(coco_json, "r") as f:
        data = json.load(f)

    annotations = data.get("annotations", [])
    annotated_image_ids = {ann["image_id"] for ann in annotations}

    original_count = len(data.get("images", []))
    data["images"] = [
        img for img in data.get("images", []) if img["id"] in annotated_image_ids
    ]

    ann_dir = output_dir / "annotations"
    ann_dir.mkdir(parents=True, exist_ok=True)
    target_json = ann_dir / coco_json.name
    with open(target_json, "w") as f:
        json.dump(data, f)

    print(f"Filtered {original_count} -> {len(data['images'])} images.")


def download_coco_images(
    input_dir: Path,
    output_dir: Path,
    nas_path: Path,
    nas_prefix: str,
    jobs: int = 8,
):
    """Downloads (copies) images from NAS to local directory based on COCO annotations."""
    coco_json = find_file(input_dir, ["*.json"])
    if not coco_json:
        raise FileNotFoundError(f"No COCO JSON found in {input_dir}")

    with open(coco_json, "r") as f:
        data = json.load(f)

    # CVAT default export structure puts images under images/default/
    base_img_dir = output_dir / "images" / "default"

    images = data.get("images", [])

    def _download_worker(img_info):
        file_name = img_info["file_name"]
        clean_rel_p = strip_prefix(file_name, nas_prefix)
        src_path = (nas_path / clean_rel_p).resolve()
        dst_path = (base_img_dir / file_name).resolve()

        if not src_path.exists():
            return False

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        return True

    print(f"Downloading {len(images)} images from NAS...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        list(executor.map(_download_worker, images))

    ann_dir = output_dir / "annotations"
    ann_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(coco_json, ann_dir / coco_json.name)
    print(f"Dataset images downloaded to {base_img_dir} and annotations to {ann_dir}")
