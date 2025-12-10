import argparse
import tempfile
import sys
import zipfile
from pathlib import Path

import yaml


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
        device=device,
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
        print(
            f"Extracting dataset to temporary directory: {tmpdir_path}", file=sys.stderr
        )
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmpdir_path)

        data_yaml_path = find_yaml_file(tmpdir_path)
        
        clean_yaml_path = filter_auto_annotations(data_yaml_path, tmpdir_path)
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
        default="0",
        help="Device to use: '0' for GPU, 'cpu' for CPU. Default: 0",
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
