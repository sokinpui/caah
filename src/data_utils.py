import random
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Annotated

import typer
import yaml

from utils import CONTEXT_SETTINGS

data_app = typer.Typer(help="Dataset utilities.", context_settings=CONTEXT_SETTINGS)


@data_app.command("split")
def run_data_split(
    dataset: Annotated[
        Path, typer.Option("--dataset", "-d", help="Path to dataset zip.")
    ],
    output: Annotated[
        Path, typer.Option("--output", "-o", help="Path for output zip.")
    ],
    split_ratio: Annotated[
        str, typer.Option("--split", "-s", help="Ratio (e.g., 80:20).")
    ],
):
    """Executes the split logic and zips the result."""
    if not dataset.is_file():
        print(f"Error: Dataset not found at {dataset}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        extract_dir, split_dir = tmpdir_path / "extracted", tmpdir_path / "split"
        for d in [extract_dir, split_dir]:
            d.mkdir()

        with zipfile.ZipFile(dataset, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        split_dataset(extract_dir, split_dir, split_ratio)

        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zipf:
            for entry in split_dir.rglob("*"):
                zipf.write(entry, entry.relative_to(split_dir))

    print(output)


def split_dataset(
    source_dir: Path, dest_dir: Path, split_str: str, nas_path: str = None
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


def _copy_split_files(pairs, img_dest, lbl_dest, only_labels=False):
    img_dest.mkdir(parents=True, exist_ok=True)
    lbl_dest.mkdir(parents=True, exist_ok=True)
    for img_path, lbl_path in pairs:
        # If using NAS, we don't copy images, we symlink them so YOLO can find them
        if only_labels:
            (img_dest / img_path.name).symlink_to(img_path)
        else:
            shutil.copy(img_path, img_dest / img_path.name)

        shutil.copy(lbl_path, lbl_dest / lbl_path.name)
