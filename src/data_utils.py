import random
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import yaml


def split_dataset(
    source_dir: Path, dest_dir: Path, split_str: str, nas_path: Optional[str] = None
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
        for ext in image_extensions:
            img_p = search_dir / rel_lp.with_suffix(ext)
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
    yaml_files = list(extracted_path.glob("**/*.yaml"))
    if yaml_files:
        with open(yaml_files[0], "r") as f:
            data = yaml.safe_load(f)
            if "names" in data:
                names = data["names"]
                return (
                    names
                    if isinstance(names, list)
                    else [n for i, n in sorted(names.items())]
                )

    names_files = list(extracted_path.glob("**/*.names"))
    if names_files:
        return names_files[0].read_text().strip().split("\n")

    raise FileNotFoundError("Could not find class names file (*.yaml or *.names).")


def _copy_split_files(
    pairs: List[Tuple[Path, Path]],
    img_dest: Path,
    lbl_dest: Path,
    only_labels: bool = False,
) -> None:
    img_dest.mkdir(parents=True, exist_ok=True)
    lbl_dest.mkdir(parents=True, exist_ok=True)
    for img_path, lbl_path in pairs:
        # If using NAS, we don't copy images, we symlink them so YOLO can find them
        if only_labels:
            (img_dest / img_path.name).symlink_to(img_path)
        else:
            shutil.copy(img_path, img_dest / img_path.name)

        shutil.copy(lbl_path, lbl_dest / lbl_path.name)
