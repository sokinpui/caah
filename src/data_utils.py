import argparse
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
        "split", help="Split a dataset into train/val sets."
    )
    add_split_arguments(split_parser)
    split_parser.set_defaults(func=run_split)


def add_split_arguments(parser):
    """Adds split-specific arguments to the parser."""
    parser.add_argument(
        "-d",
        "--dataset",
        required=True,
        help="Path to the input dataset zip file (YOLO 1.1 format).",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Path for the output dataset zip file.",
    )
    parser.add_argument(
        "-s",
        "--split",
        required=True,
        type=str,
        help="Train:Val split ratio (e.g., '80:20').",
    )


def _find_class_names(extracted_path: Path) -> list[str]:
    """Finds and parses the class names file (e.g., obj.names, data.yaml)."""
    # Prefer data.yaml
    yaml_files = list(extracted_path.glob("**/*.yaml"))
    if yaml_files:
        with open(yaml_files[0], "r") as f:
            data = yaml.safe_load(f)
            if "names" in data and isinstance(data["names"], list):
                return data["names"]
            if "names" in data and isinstance(data["names"], dict):
                # Handle dict format {0: 'name1', 1: 'name2'}
                return [name for i, name in sorted(data["names"].items())]

    # Fallback to .names file
    names_files = list(extracted_path.glob("**/*.names"))
    if names_files:
        return names_files[0].read_text().strip().split("\n")

    raise FileNotFoundError(
        "Could not find a class names file (*.yaml or *.names) in the dataset."
    )


def run_split(args):
    """Splits a YOLO dataset into training and validation sets."""
    dataset_zip = Path(args.dataset)
    output_zip_path = Path(args.output)

    if not dataset_zip.is_file() or dataset_zip.suffix.lower() != ".zip":
        print(
            f"Error: --dataset must be a valid zip file. Got: {dataset_zip}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        train_ratio_str, val_ratio_str = args.split.split(":")
        train_ratio = int(train_ratio_str)
        val_ratio = int(val_ratio_str)
        total = train_ratio + val_ratio
        if total <= 0:
            raise ValueError("Sum of ratios must be positive.")
        train_frac = train_ratio / total
    except ValueError:
        print(
            f"Error: Invalid split ratio '{args.split}'. Must be in 'train:val' format (e.g., '80:20').",
            file=sys.stderr,
        )
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        extract_dir = tmpdir_path / "input"
        extract_dir.mkdir()
        build_dir = tmpdir_path / "output"
        build_dir.mkdir()

        print(
            f"Extracting {dataset_zip.name} to a temporary directory...",
            file=sys.stderr,
        )
        with zipfile.ZipFile(dataset_zip, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
        image_paths = [
            p for p in extract_dir.rglob("*") if p.suffix.lower() in image_extensions
        ]

        if not image_paths:
            print("Error: No images found in the dataset.", file=sys.stderr)
            sys.exit(1)

        class_names = _find_class_names(extract_dir)
        print(f"Found {len(class_names)} classes: {class_names}", file=sys.stderr)

        random.shuffle(image_paths)
        split_idx = int(len(image_paths) * train_frac)
        train_images = image_paths[:split_idx]
        val_images = image_paths[split_idx:]

        print(
            f"Splitting dataset: {len(train_images)} train, {len(val_images)} val.",
            file=sys.stderr,
        )

        # Create output structure
        train_img_dir = build_dir / "images" / "train"
        val_img_dir = build_dir / "images" / "val"
        train_lbl_dir = build_dir / "labels" / "train"
        val_lbl_dir = build_dir / "labels" / "val"

        for d in [train_img_dir, val_img_dir, train_lbl_dir, val_lbl_dir]:
            d.mkdir(parents=True, exist_ok=True)

        # Copy files
        def copy_files(image_list, img_dest, lbl_dest):
            for img_path in image_list:
                lbl_path = img_path.with_suffix(".txt")
                if not lbl_path.exists():
                    print(
                        f"Warning: Label file not found for {img_path.name}, skipping.",
                        file=sys.stderr,
                    )
                    continue
                shutil.copy(img_path, img_dest / img_path.name)
                shutil.copy(lbl_path, lbl_dest / lbl_path.name)

        print("Copying training files...", file=sys.stderr)
        copy_files(train_images, train_img_dir, train_lbl_dir)
        print("Copying validation files...", file=sys.stderr)
        copy_files(val_images, val_img_dir, val_lbl_dir)

        # Create data.yaml
        yaml_data = {
            "train": "images/train",
            "val": "images/val",
            "names": {i: name for i, name in enumerate(class_names)},
        }
        yaml_path = build_dir / "data.yaml"
        with open(yaml_path, "w") as f:
            yaml.dump(yaml_data, f, sort_keys=False)

        print(f"Created {yaml_path}", file=sys.stderr)

        print(f"Zipping output directory to {output_zip_path}...", file=sys.stderr)
        zip_output_path_str = shutil.make_archive(
            base_name=str(output_zip_path.with_suffix("")),
            format="zip",
            root_dir=str(build_dir),
        )
        final_path = Path(zip_output_path_str)

    print(final_path)
