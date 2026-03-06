import json
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Tuple

from datumaro.components.dataset import Dataset

from utils import create_zip, extract_zip


def slice_coco_dataset(
    input_zip: Path,
    output_zip: Path,
    slice_size: Tuple[int, int] = (640, 640),
    overlap_ratio: Tuple[float, float] = (0.2, 0.2),
):
    """
    Slices a COCO dataset into tiles using SAHI.
    """
    from sahi.slicing import slice_coco

    if not input_zip.is_file():
        raise FileNotFoundError(f"Input file not found: {input_zip}")

    with tempfile.TemporaryDirectory() as tmp_dir:
        working_dir = Path(tmp_dir)
        extract_path = working_dir / "extract"
        output_dir = working_dir / "sliced"

        ann_dir = output_dir / "annotations"
        img_dir = output_dir / "images"
        ann_dir.mkdir(parents=True, exist_ok=True)
        img_dir.mkdir(parents=True, exist_ok=True)

        extract_zip(input_zip, extract_path)

        json_files = sorted(list(extract_path.rglob("*.json")))
        if not json_files:
            raise FileNotFoundError("No COCO JSON annotation file found in the zip.")

        for coco_path in json_files:
            src_image_dir = _resolve_image_dir(extract_path, coco_path)

            # Use a temporary subdir to catch SAHI output and avoid name collisions
            with tempfile.TemporaryDirectory() as slice_tmp:
                slice_tmp_path = Path(slice_tmp)

                slice_coco(
                    coco_annotation_file_path=str(coco_path),
                    image_dir=str(src_image_dir),
                    output_coco_annotation_file_name=coco_path.name,
                    output_dir=str(slice_tmp_path),
                    slice_height=slice_size[0],
                    slice_width=slice_size[1],
                    overlap_height_ratio=overlap_ratio[0],
                    overlap_width_ratio=overlap_ratio[1],
                )

                # Move generated JSONs to annotations/
                for gj in slice_tmp_path.glob("*.json"):
                    shutil.move(str(gj), str(ann_dir / gj.name))

                # Move images to images/
                for item in slice_tmp_path.iterdir():
                    if item.is_dir():
                        shutil.copytree(item, img_dir / item.name, dirs_exist_ok=True)
                    elif item.is_file() and item.suffix.lower() != ".json":
                        shutil.move(str(item), str(img_dir / item.name))

        create_zip(output_dir, output_zip)


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


def coco_to_yolo(input_zip: Path, output_zip: Path):
    """
    Converts a COCO format ZIP dataset to YOLO format.
    """
    if not input_zip.is_file():
        raise FileNotFoundError(f"Input file not found: {input_zip}")

    with tempfile.TemporaryDirectory() as tmp_dir:
        working_dir = Path(tmp_dir)
        extract_path = working_dir / "extract"
        export_path = working_dir / "export"

        extract_zip(input_zip, extract_path)

        dataset = Dataset.import_from(str(extract_path), format="coco")
        dataset.export(str(export_path), format="yolo", save_media=True)

        create_zip(export_path, output_zip)


def yolo_to_coco(
    input_zip: Path,
    output_zip: Path,
    nas_path: Optional[Path] = None,
    nas_prefix: str = "",
):
    """
    Converts a YOLO format ZIP dataset to COCO instances format.
    Handles datasets with or without images automatically via Datumaro.
    """
    if not input_zip.is_file():
        raise FileNotFoundError(f"Input file not found: {input_zip}")

    with tempfile.TemporaryDirectory() as tmp_dir:
        working_dir = Path(tmp_dir)
        extract_path = working_dir / "extract"
        export_path = working_dir / "export"

        extract_zip(input_zip, extract_path)

        if nas_path:
            _fill_images_from_nas(extract_path, nas_path, nas_prefix)

        dataset = Dataset.import_from(str(extract_path), format="yolo")
        dataset.export(str(export_path), format="coco_instances", save_media=True)

        create_zip(export_path, output_zip)


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
