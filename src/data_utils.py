import concurrent.futures
import json
import os
import random
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import yaml
from ultralytics.data.split import autosplit

from utils import find_file, strip_prefix


def _parse_split_ratio(split_str: str) -> List[int]:
    """Parses split ratio string into list of integers."""
    try:
        parts = [int(v) for v in split_str.split(":")]
        if len(parts) == 2 and sum(parts) > 0:
            return parts
    except (ValueError, IndexError, ZeroDivisionError):
        pass
    raise ValueError(f"Invalid split ratio '{split_str}'. Expected 'train:val' (e.g. 8:2)")


def split_coco_dataset(
    source_dir: Path,
    dest_dir: Path,
    split_str: str,
    nas_path: Optional[str] = None,
    nas_prefix: str = "",
) -> Path:
    """Splits a COCO dataset into train/val sets by partitioning the JSON."""
    ratios = _parse_split_ratio(split_str)
    train_frac = ratios[0] / sum(ratios)

    coco_json = find_file(source_dir, ["*.json"])
    if not coco_json:
        raise FileNotFoundError(f"No COCO JSON found in {source_dir}")

    with open(coco_json, "r") as f:
        data = json.load(f)

    images = data.get("images", [])
    annotations = data.get("annotations", [])
    categories = data.get("categories", [])

    random.shuffle(images)
    split_idx = int(len(images) * train_frac)

    train_images = images[:split_idx]
    val_images = images[split_idx:]

    def _filter_coco(selected_images):
        img_ids = {img["id"] for img in selected_images}
        return {
            "images": selected_images,
            "annotations": [ann for ann in annotations if ann["image_id"] in img_ids],
            "categories": categories,
        }

    train_data = _filter_coco(train_images)
    val_data = _filter_coco(val_images)

    # Setup directory structure
    (dest_dir / "annotations").mkdir(parents=True, exist_ok=True)
    (dest_dir / "images" / "train").mkdir(parents=True, exist_ok=True)
    (dest_dir / "images" / "val").mkdir(parents=True, exist_ok=True)

    with open(dest_dir / "annotations" / "instances_train.json", "w") as f:
        json.dump(train_data, f)
    with open(dest_dir / "annotations" / "instances_val.json", "w") as f:
        json.dump(val_data, f)

    # Build index for fast lookup
    file_index = _index_directory(source_dir if not nas_path else Path(nas_path))

    _prepare_coco_images(
        train_images,
        source_dir,
        dest_dir / "images" / "train",
        file_index,
        nas_path,
        nas_prefix,
    )
    _prepare_coco_images(
        val_images,
        source_dir,
        dest_dir / "images" / "val",
        file_index,
        nas_path,
        nas_prefix,
    )

    yaml_path = dest_dir / "data.yaml"
    yaml_data = {
        "path": str(dest_dir.absolute()),
        "train": "images/train",
        "val": "images/val",
        "names": {cat["id"]: cat["name"] for cat in categories},
    }

    # Note: categories in COCO can start at 1, but YOLO expects 0-indexed.
    # If categories are 1-indexed, we shift them for the YAML names mapping.
    cat_ids = [cat["id"] for cat in categories]
    if cat_ids and min(cat_ids) == 1:
        yaml_data["names"] = {cat["id"] - 1: cat["name"] for cat in categories}
    else:
        yaml_data["names"] = {i: cat["name"] for i, cat in enumerate(categories)}

    with open(yaml_path, "w") as f:
        yaml.dump(yaml_data, f, sort_keys=False)

    return yaml_path


def split_dataset(
    source_dir: Path,
    dest_dir: Path,
    split_str: str,
    nas_path: Optional[str] = None,
    nas_prefix: str = "",
) -> Path:
    """Splits YOLO dataset files into train/val sets."""
    ratios = _parse_split_ratio(split_str)
    total = sum(ratios)
    weights = (ratios[0] / total, ratios[1] / total, 0.0)
    labels_root = (
        source_dir / "obj_train_data"
        if (source_dir / "obj_train_data").is_dir()
        else source_dir
    )
    search_dir = Path(nas_path) if nas_path else labels_root

    autosplit(path=search_dir, weights=weights, annotated_only=False)

    label_index = _index_directory(labels_root, [".txt"])

    for split_name in ["train", "val"]:
        split_file = search_dir.parent / f"autosplit_{split_name}.txt"
        if not split_file.exists():
            continue

        with open(split_file, "r") as f:
            img_paths = [search_dir.parent / line.strip() for line in f if line.strip()]

        pairs = _match_labels_to_images(img_paths, label_index)
        _copy_split_files(
            pairs,
            dest_dir / "images" / split_name,
            dest_dir / "labels" / split_name,
            only_labels=bool(nas_path),
        )
        split_file.unlink()

    yaml_path = dest_dir / "data.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(
            {
                "train": "images/train",
                "val": "images/val",
                "names": {i: n for i, n in enumerate(find_class_names(source_dir))},
            },
            f,
            sort_keys=False,
        )
    return yaml_path


def find_class_names(extracted_path: Path) -> list[str]:
    """Finds class names from data.yaml or obj.names."""
    yaml_file = find_file(extracted_path, ["*.yaml"])
    if yaml_file:
        with open(yaml_file, "r") as f:
            names = yaml.safe_load(f).get("names")
            if names:
                return (
                    names
                    if isinstance(names, list)
                    else [n for i, n in sorted(names.items())]
                )

    names_file = find_file(extracted_path, ["*.names", "classes.txt"])
    if names_file:
        return names_file.read_text().strip().split("\n")

    raise FileNotFoundError(
        "Could not find class names file (*.yaml, *.names, or classes.txt)."
    )


def _match_labels_to_images(
    img_paths: List[Path], label_index: dict
) -> List[Tuple[Path, Path]]:
    pairs = []
    for img_p in img_paths:
        lbl_p = label_index.get(f"{img_p.stem}.txt")
        if lbl_p:
            pairs.append((img_p, lbl_p))
    return pairs


def _copy_split_files(
    pairs: List[Tuple[Path, Path]],
    img_dest: Path,
    lbl_dest: Path,
    only_labels: bool = False,
) -> None:
    img_dest.mkdir(parents=True, exist_ok=True)
    lbl_dest.mkdir(parents=True, exist_ok=True)

    def _worker(idx_pair):
        i, (img_path, lbl_path) = idx_pair
        unique_stem = f"{i}_{img_path.stem}"
        target_img = img_dest / f"{unique_stem}{img_path.suffix}"
        target_lbl = lbl_dest / f"{unique_stem}{lbl_path.suffix}"

        if only_labels:
            target_img.symlink_to(img_path)
        else:
            shutil.copy(img_path, target_img)
        shutil.copy(lbl_path, target_lbl)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(executor.map(_worker, enumerate(pairs)))


def _prepare_coco_images(
    images: List[dict],
    source_dir: Path,
    dest_img_dir: Path,
    file_index: dict[str, Path],
    nas_path: Optional[str] = None,
    nas_prefix: str = "",
) -> None:
    """Copies or symlinks images for a COCO split."""

    def _worker(img_info):
        file_name = img_info["file_name"]
        img_name = Path(file_name).name

        # Priority 1: Direct path
        src_img = source_dir / file_name
        if src_img.exists():
            _link_or_copy(src_img, dest_img_dir / img_name, bool(nas_path))
            return

        # Priority 2: Indexed lookup
        if img_name in file_index:
            _link_or_copy(file_index[img_name], dest_img_dir / img_name, bool(nas_path))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(executor.map(_worker, images))


def _index_directory(
    directory: Path, extensions: Optional[List[str]] = None
) -> dict[str, Path]:
    """Creates a mapping of filenames to their absolute paths."""
    index = {}
    ext_set = {e.lower() for e in extensions} if extensions else None
    for p in directory.rglob("*"):
        if not p.is_file():
            continue
        if ext_set and p.suffix.lower() not in ext_set:
            continue
        index[p.name] = p
    return index


def _link_or_copy(src: Path, dst: Path, use_symlink: bool):
    """Helper to symlink or copy a file."""
    if dst.exists():
        return
    if use_symlink:
        dst.symlink_to(src)
    else:
        shutil.copy(src, dst)
