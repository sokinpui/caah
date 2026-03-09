import json
import os
import random
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import yaml

from utils import find_file, strip_prefix


def split_coco_dataset(
    source_dir: Path,
    dest_dir: Path,
    split_str: str,
    nas_path: Optional[str] = None,
    nas_prefix: str = "",
) -> Path:
    """Splits a COCO dataset into train/val sets by partitioning the JSON."""
    try:
        train_ratio_str, val_ratio_str = split_str.split(":")
        train_frac = int(train_ratio_str) / (int(train_ratio_str) + int(val_ratio_str))
    except (ValueError, ZeroDivisionError):
        print(f"Error: Invalid split ratio '{split_str}'.", file=sys.stderr)
        sys.exit(1)

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

    _prepare_coco_images(
        train_images, source_dir, dest_dir / "images" / "train", nas_path, nas_prefix
    )
    _prepare_coco_images(
        val_images, source_dir, dest_dir / "images" / "val", nas_path, nas_prefix
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
    """Splits files from source_dir into train/val sets in dest_dir."""
    try:
        train_ratio_str, val_ratio_str = split_str.split(":")
        train_frac = int(train_ratio_str) / (int(train_ratio_str) + int(val_ratio_str))
    except (ValueError, ZeroDivisionError):
        print(f"Error: Invalid split ratio '{split_str}'.", file=sys.stderr)
        sys.exit(1)

    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]

    labels_root = (
        source_dir / "obj_train_data"
        if (source_dir / "obj_train_data").is_dir()
        else source_dir
    )
    search_dir = Path(nas_path) if nas_path else labels_root

    label_paths = list(labels_root.rglob("*.txt"))

    image_label_pairs = []
    for lp in label_paths:
        rel_lp = lp.relative_to(labels_root)
        rel_lp_str = str(rel_lp)

        # Strip prefix to find in NAS
        clean_rel_p = strip_prefix(rel_lp_str, nas_prefix)

        for ext in image_extensions:
            img_p = search_dir / Path(clean_rel_p).with_suffix(ext)
            if img_p.exists():
                image_label_pairs.append((img_p, lp))
                break

    if not image_label_pairs:
        print(f"Error: No matching images found in {search_dir}.", file=sys.stderr)
        sys.exit(1)

    class_names = find_class_names(source_dir)
    random.shuffle(image_label_pairs)
    split_idx = int(len(image_label_pairs) * train_frac)

    _copy_split_files(
        image_label_pairs[:split_idx],
        dest_dir / "images" / "train",
        dest_dir / "labels" / "train",
        only_labels=bool(nas_path),
    )
    _copy_split_files(
        image_label_pairs[split_idx:],
        dest_dir / "images" / "val",
        dest_dir / "labels" / "val",
        only_labels=bool(nas_path),
    )

    yaml_path = dest_dir / "data.yaml"
    yaml_data = {
        "train": "images/train",
        "val": "images/val",
        "names": {i: name for i, name in enumerate(class_names)},
    }

    # If using NAS, we point the base path to the NAS, but labels are local.
    # However, Ultralytics expects images/ and labels/ to be siblings.
    # So we keep paths relative to the temp 'split' directory.

    with open(yaml_path, "w") as f:
        yaml.dump(yaml_data, f, sort_keys=False)

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


def _copy_split_files(
    pairs: List[Tuple[Path, Path]],
    img_dest: Path,
    lbl_dest: Path,
    only_labels: bool = False,
) -> None:
    img_dest.mkdir(parents=True, exist_ok=True)
    lbl_dest.mkdir(parents=True, exist_ok=True)
    for i, (img_path, lbl_path) in enumerate(pairs):
        unique_stem = f"{i}_{img_path.stem}"
        target_img = img_dest / f"{unique_stem}{img_path.suffix}"
        target_lbl = lbl_dest / f"{unique_stem}{lbl_path.suffix}"

        # If using NAS, we don't copy images, we symlink them so YOLO can find them
        if only_labels:
            target_img.symlink_to(img_path)
        else:
            shutil.copy(img_path, target_img)
        shutil.copy(lbl_path, target_lbl)


def _prepare_coco_images(
    images: List[dict],
    source_dir: Path,
    dest_img_dir: Path,
    nas_path: Optional[str] = None,
    nas_prefix: str = "",
) -> None:
    """Copies or symlinks images for a COCO split."""
    search_dir = Path(nas_path) if nas_path else source_dir

    for img_info in images:
        file_name = img_info["file_name"]

        # Try to find the image in source_dir first, then NAS
        src_img = find_file(source_dir, [file_name, f"**/{file_name}"])

        if not src_img and nas_path:
            clean_rel_p = strip_prefix(file_name, nas_prefix)
            src_img = Path(nas_path) / clean_rel_p

        if not src_img or not src_img.exists():
            continue

        target = dest_img_dir / Path(file_name).name
        target.symlink_to(src_img) if nas_path else shutil.copy(src_img, target)
