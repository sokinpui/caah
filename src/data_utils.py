import random
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml


def setup_data_parser(parser):
    """Adds data utility subcommands to the parser."""
    subparsers = parser.add_subparsers(
        dest="action", required=True, help="Available data commands"
    )

    split_parser = subparsers.add_parser(
        "split", help="Split a YOLO dataset into train and val sets."
    )
    split_parser.add_argument(
        "-d", "--dataset", required=True, help="Path to the input dataset zip file."
    )
    split_parser.add_argument(
        "-o", "--output", required=True, help="Path for the output dataset zip file."
    )
    split_parser.add_argument(
        "-s",
        "--split",
        required=True,
        help="Train:Val split ratio (e.g., '80:20').",
    )
    split_parser.set_defaults(func=run_data_split)


def run_data_split(args):
    """Executes the split logic and zips the result."""
    input_zip = Path(args.dataset)
    output_zip = Path(args.output)

    if not input_zip.is_file():
        print(f"Error: Dataset not found at {input_zip}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        extract_dir = tmpdir_path / "extracted"
        split_dir = tmpdir_path / "split"
        extract_dir.mkdir()
        split_dir.mkdir()

        with zipfile.ZipFile(input_zip, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        split_dataset(extract_dir, split_dir, args.split)

        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for entry in split_dir.rglob("*"):
                zipf.write(entry, entry.relative_to(split_dir))

    print(output_zip)


def split_dataset(source_dir: Path, dest_dir: Path, split_str: str) -> Path:
    """Splits files from source_dir into train/val sets in dest_dir."""
    try:
        train_ratio_str, val_ratio_str = split_str.split(":")
        train_frac = int(train_ratio_str) / (int(train_ratio_str) + int(val_ratio_str))
    except (ValueError, ZeroDivisionError):
        print(f"Error: Invalid split ratio '{split_str}'.", file=sys.stderr)
        sys.exit(1)

    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
    image_paths = [
        p for p in source_dir.rglob("*") if p.suffix.lower() in image_extensions
    ]

    if not image_paths:
        print("Error: No images found to split.", file=sys.stderr)
        sys.exit(1)

    class_names = find_class_names(source_dir)
    random.shuffle(image_paths)
    split_idx = int(len(image_paths) * train_frac)

    _copy_split_files(
        image_paths[:split_idx],
        dest_dir / "images" / "train",
        dest_dir / "labels" / "train",
    )
    _copy_split_files(
        image_paths[split_idx:],
        dest_dir / "images" / "val",
        dest_dir / "labels" / "val",
    )

    yaml_path = dest_dir / "data.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(
            {
                "train": "./images/train",
                "val": "./images/val",
                "names": {i: name for i, name in enumerate(class_names)},
            },
            f,
            sort_keys=False,
        )
    return yaml_path


def find_class_names(extracted_path: Path) -> list[str]:
    """Finds class names from data.yaml or obj.names."""
    yaml_files = list(extracted_path.glob("**/*.yaml"))
    if yaml_files:
        with open(yaml_files[0], "r") as f:
            data = yaml.safe_load(f)
            if "names" in data:
                names = data["names"]
                return names if isinstance(names, list) else [n for i, n in sorted(names.items())]

    names_files = list(extracted_path.glob("**/*.names"))
    if names_files:
        return names_files[0].read_text().strip().split("\n")

    raise FileNotFoundError("Could not find class names file (*.yaml or *.names).")


def _copy_split_files(image_list, img_dest, lbl_dest):
    img_dest.mkdir(parents=True, exist_ok=True)
    lbl_dest.mkdir(parents=True, exist_ok=True)
    for img_path in image_list:
        lbl_path = img_path.with_suffix(".txt")
        if lbl_path.exists():
            shutil.copy(img_path, img_dest / img_path.name)
            shutil.copy(lbl_path, lbl_dest / lbl_path.name)
