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

    unpick_parser = subparsers.add_parser(
        "unpick", help="Separate manual and auto annotations into different datasets."
    )
    add_unpick_arguments(unpick_parser)
    unpick_parser.set_defaults(func=run_unpick)


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


def add_unpick_arguments(parser):
    """Adds unpick-specific arguments."""
    parser.add_argument(
        "-i", "--input", required=True, help="Path to input mixed dataset zip."
    )
    parser.add_argument(
        "-m", "--manual-output", required=True, help="Path for manual output zip."
    )
    parser.add_argument(
        "-a", "--auto-output", required=True, help="Path for auto output zip."
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


def run_unpick(args):
    """Separates manual and auto annotations into two zip files."""
    input_zip = Path(args.input)
    manual_zip = Path(args.manual_output)
    auto_zip = Path(args.auto_output)

    if not input_zip.is_file():
        print(f"Error: Input file not found: {input_zip}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        source_dir = tmpdir_path / "source"
        manual_dir = tmpdir_path / "manual"
        auto_dir = tmpdir_path / "auto"
        
        source_dir.mkdir()
        manual_dir.mkdir()
        auto_dir.mkdir()

        print(f"Extracting {input_zip.name}...", file=sys.stderr)
        with zipfile.ZipFile(input_zip, "r") as zip_ref:
            zip_ref.extractall(source_dir)

        # 1. Parse data.yaml to build mappings
        yaml_files = list(source_dir.glob("**/data.yaml"))
        if not yaml_files:
            print("Error: data.yaml not found in dataset.", file=sys.stderr)
            sys.exit(1)
        
        original_yaml_path = yaml_files[0]
        with open(original_yaml_path, "r") as f:
            data_config = yaml.safe_load(f)

        names_obj = data_config.get("names", [])
        # Normalize to dict {id: name}
        if isinstance(names_obj, list):
            original_names = {i: n for i, n in enumerate(names_obj)}
        elif isinstance(names_obj, dict):
            original_names = {int(k): v for k, v in names_obj.items()}
        else:
            print("Error: Unknown format for 'names' in data.yaml", file=sys.stderr)
            sys.exit(1)

        manual_names = []
        auto_names = []
        map_manual = {} # old_id -> new_id
        map_auto = {}   # old_id -> new_id

        for idx, name in sorted(original_names.items()):
            if name.endswith(" (auto)"):
                map_auto[idx] = len(auto_names)
                auto_names.append(name)
            else:
                map_manual[idx] = len(manual_names)
                manual_names.append(name)

        print(f"Found {len(manual_names)} manual classes and {len(auto_names)} auto classes.", file=sys.stderr)

        # 2. Process files
        # We walk through source_dir.
        # Images: copy to both.
        # Labels: split and rewrite.
        # Other (yaml): handle separately.

        for item in source_dir.rglob("*"):
            if not item.is_file():
                continue
            
            rel_path = item.relative_to(source_dir)
            
            # Skip the original yaml, we will create new ones
            if item.name == "data.yaml":
                continue

            suffix = item.suffix.lower()
            
            # Prepare destinations
            m_dest = manual_dir / rel_path
            a_dest = auto_dir / rel_path
            m_dest.parent.mkdir(parents=True, exist_ok=True)
            a_dest.parent.mkdir(parents=True, exist_ok=True)

            if suffix == ".txt" and "labels" in item.parts:
                # Process Label File
                with open(item, "r") as f:
                    lines = f.readlines()
                
                m_lines = []
                a_lines = []
                
                for line in lines:
                    parts = line.strip().split()
                    if not parts: continue
                    try:
                        cls_id = int(parts[0])
                        rest = " ".join(parts[1:])
                        if cls_id in map_manual:
                            m_lines.append(f"{map_manual[cls_id]} {rest}\n")
                        if cls_id in map_auto:
                            a_lines.append(f"{map_auto[cls_id]} {rest}\n")
                    except ValueError:
                        pass # Skip invalid lines

                if m_lines:
                    with open(m_dest, "w") as f: f.writelines(m_lines)
                if a_lines:
                    with open(a_dest, "w") as f: f.writelines(a_lines)
            else:
                # Copy Image or other file (e.g. README)
                shutil.copy2(item, m_dest)
                shutil.copy2(item, a_dest)

        # 3. Create new data.yaml files
        def write_yaml(path, names_list):
            # Use relative paths common in YOLO structure
            # Assuming standard structure exists, else reuse source keys if possible? 
            # Safest is to reuse source config but replace names/nc
            new_config = data_config.copy()
            new_config["names"] = names_list
            new_config["nc"] = len(names_list)
            with open(path, "w") as f:
                yaml.dump(new_config, f, sort_keys=False)

        write_yaml(manual_dir / "data.yaml", manual_names)
        write_yaml(auto_dir / "data.yaml", auto_names)

        # 4. Zip results
        print(f"Creating manual zip at {manual_zip}...", file=sys.stderr)
        shutil.make_archive(str(manual_zip.with_suffix("")), "zip", manual_dir)
        
        print(f"Creating auto zip at {auto_zip}...", file=sys.stderr)
        shutil.make_archive(str(auto_zip.with_suffix("")), "zip", auto_dir)

    print(f"{manual_zip}\n{auto_zip}")
