import argparse
import tempfile
import sys
import zipfile
import random
import shutil
from pathlib import Path

import yaml


def _resolve_device(device: str) -> str:
    """Resolves the device string to a valid torch/ultralytics device."""
    import torch

    if device == "cpu":
        return "cpu"
    if device == "gpu":
        if torch.cuda.is_available():
            return "cuda"
        if torch.backends.mps.is_available():
            return "mps"
        print(
            "Warning: GPU requested but not available. Falling back to CPU.",
            file=sys.stderr,
        )
        return "cpu"
    return device


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


def find_yaml_file(directory: Path) -> Path:
    """
    Finds the 'data.yaml' file in the extracted directory.
    Raises FileNotFoundError if not found.
    """
    yaml_files = list(directory.glob("**/data.yaml"))
    if not yaml_files:
        raise FileNotFoundError(f"Could not find 'data.yaml' in {directory}")
    if len(yaml_files) > 1:
        print(
            f"Warning: Found multiple 'data.yaml' files. Using the first one: {yaml_files[0]}",
            file=sys.stderr,
        )
    return yaml_files[0]


def _split_dataset(source_dir: Path, dest_dir: Path, split_str: str) -> Path:
    """Splits files from source_dir into train/val sets in dest_dir."""
    try:
        train_ratio_str, val_ratio_str = split_str.split(":")
        train_ratio = int(train_ratio_str)
        val_ratio = int(val_ratio_str)
        total = train_ratio + val_ratio
        if total <= 0:
            raise ValueError("Sum of ratios must be positive.")
        train_frac = train_ratio / total
    except ValueError:
        print(
            f"Error: Invalid split ratio '{split_str}'. Must be in 'train:val' format (e.g., '80:20').",
            file=sys.stderr,
        )
        sys.exit(1)

    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
    image_paths = [
        p for p in source_dir.rglob("*") if p.suffix.lower() in image_extensions
    ]

    if not image_paths:
        print("Error: No images found in the dataset to split.", file=sys.stderr)
        sys.exit(1)

    class_names = _find_class_names(source_dir)
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
    train_img_dir = dest_dir / "images" / "train"
    val_img_dir = dest_dir / "images" / "val"
    train_lbl_dir = dest_dir / "labels" / "train"
    val_lbl_dir = dest_dir / "labels" / "val"

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
        "train": "../images/train",
        "val": "../images/val",
        "names": {i: name for i, name in enumerate(class_names)},
    }
    yaml_path = dest_dir / "data.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_data, f, sort_keys=False)

    print(f"Created {yaml_path}", file=sys.stderr)
    return yaml_path


def filter_auto_annotations(yaml_path: Path, root_dir: Path):
    """
    Removes classes ending with ' (auto)' from data.yaml and
    removes/remaps corresponding annotations in label files.
    """
    print("Checking for auto-annotations to filter...", file=sys.stderr)
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    names = data.get("names")
    if not names:
        return yaml_path

    # Standardize names to a dictionary {index: name} for processing
    if isinstance(names, list):
        names_dict = {i: n for i, n in enumerate(names)}
    elif isinstance(names, dict):
        names_dict = {int(k): v for k, v in names.items()}
    else:
        print(
            "Warning: Unknown format for 'names' in data.yaml. Skipping filtering.",
            file=sys.stderr,
        )
        return yaml_path

    # Identify which IDs to keep and which to drop
    keep_map = {}  # old_id -> new_id
    new_names_list = []

    sorted_ids = sorted(names_dict.keys())

    for old_id in sorted_ids:
        name = names_dict[old_id]
        if str(name).endswith(" (auto)"):
            continue  # Drop this class

        # Keep this class
        new_id = len(new_names_list)
        keep_map[old_id] = new_id
        new_names_list.append(name)

    # If no changes needed
    if len(new_names_list) == len(sorted_ids):
        print("No auto-annotations found.", file=sys.stderr)
        return yaml_path

    print(
        f"Filtering auto-annotations. Reduced classes from {len(sorted_ids)} to {len(new_names_list)}.",
        file=sys.stderr,
    )

    # Process all .txt files in the extracted directory
    # We look for files that look like labels (inside a 'labels' folder is a good heuristic for YOLO datasets)
    label_files = [p for p in root_dir.rglob("*.txt") if "labels" in p.parts]

    for lbl_path in label_files:
        with open(lbl_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        file_changed = False

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue

            try:
                class_id = int(parts[0])
                if class_id in keep_map:
                    new_id = keep_map[class_id]
                    if new_id != class_id:
                        parts[0] = str(new_id)
                        new_lines.append(" ".join(parts) + "\n")
                        file_changed = True
                    else:
                        new_lines.append(line)
                else:
                    # Drop this line (it's an auto annotation)
                    file_changed = True
            except ValueError:
                # Not a valid label line, keep it
                new_lines.append(line)

        if file_changed:
            with open(lbl_path, "w") as f:
                f.writelines(new_lines)

    # Update data.yaml
    data["names"] = {i: n for i, n in enumerate(new_names_list)}
    data["nc"] = len(new_names_list)

    with open(yaml_path, "w") as f:
        yaml.dump(data, f, sort_keys=False)

    print("Dataset filtering complete.", file=sys.stderr)
    return yaml_path


def train_model(
    data_yaml_path: Path,
    model_size: str,
    epochs: int,
    img_size: int,
    batch_size: int,
    device: str,
):
    """
    Initializes and trains the YOLO model.
    """
    print("--- Starting Training ---", file=sys.stderr)
    from ultralytics import YOLO

    resolved_device = _resolve_device(device)

    print(f"Data: {data_yaml_path}", file=sys.stderr)
    print(f"Model: {model_size}", file=sys.stderr)
    print(f"Epochs: {epochs}", file=sys.stderr)

    model_name = f"{model_size}.pt"
    model = YOLO(model_name)

    results = model.train(
        data=str(data_yaml_path),
        epochs=epochs,
        imgsz=img_size,
        batch=batch_size,
        device=resolved_device,
        plots=True,
        save=True,
    )

    print("--- Training Complete ---", file=sys.stderr)
    best_model_path = f"{results.save_dir}/weights/best.pt"
    print(best_model_path)


def process_dataset_and_train(
    dataset_zip_path: str,
    model_size: str,
    epochs: int,
    img_size: int,
    batch_size: int,
    device: str,
    split: str = None,
):
    """
    Extracts the dataset from a zip file and initiates the training process.
    """
    zip_path = Path(dataset_zip_path)
    if not zip_path.is_file() or zip_path.suffix.lower() != ".zip":
        raise FileNotFoundError(
            f"Error: Dataset path is not a valid zip file: {dataset_zip_path}"
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        extract_dir = tmpdir_path / "extracted"
        extract_dir.mkdir()
        print(
            f"Extracting dataset to temporary directory: {extract_dir}",
            file=sys.stderr,
        )
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        if split:
            print(f"Splitting dataset with ratio {split}...", file=sys.stderr)
            split_dir = tmpdir_path / "split"
            split_dir.mkdir()
            data_yaml_path = _split_dataset(extract_dir, split_dir, split)
            training_data_root = split_dir
        else:
            data_yaml_path = find_yaml_file(extract_dir)
            training_data_root = extract_dir

        clean_yaml_path = filter_auto_annotations(data_yaml_path, training_data_root)
        train_model(clean_yaml_path, model_size, epochs, img_size, batch_size, device)


def add_train_arguments(parser):
    """
    Adds training-specific arguments to the parser.
    """
    parser.add_argument(
        "-d",
        "--data",
        type=str,
        required=True,
        help="Path to the zipped dataset file from CVAT ('Ultralytics YOLO' format).",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="yolo11n",
        help="Model version/size (e.g., yolo11n, yolo11s, yolov8m). Default: yolo11n",
    )
    parser.add_argument(
        "-e",
        "--epochs",
        type=int,
        default=50,
        help="Number of training epochs. Default: 50",
    )
    parser.add_argument(
        "--imgsz", type=int, default=640, help="Image size (pixels). Default: 640"
    )
    parser.add_argument(
        "-b",
        "--batch",
        type=int,
        default=16,
        help="Batch size (reduce for GPU OOM errors). Default: 16",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="gpu",
        help="Device to use: 'gpu', 'cpu', or a device ID like '0'. Default: 'gpu'",
    )
    parser.add_argument(
        "-s",
        "--split",
        type=str,
        default=None,
        help="Train:Val split ratio (e.g., '80:20'). If provided, the dataset will be split before training.",
    )


def run_train(args):
    """
    Runs the training process with parsed arguments.
    """
    try:
        process_dataset_and_train(
            dataset_zip_path=args.data,
            model_size=args.model,
            epochs=args.epochs,
            img_size=args.imgsz,
            batch_size=args.batch,
            device=args.device,
            split=args.split,
        )
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)


def main():
    """
    Main function to run the training script directly.
    """
    parser = argparse.ArgumentParser(
        description="Train a YOLO model using a zipped CVAT export."
    )
    add_train_arguments(parser)
    args = parser.parse_args()
    run_train(args)


if __name__ == "__main__":
    main()
