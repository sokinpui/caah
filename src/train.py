import argparse
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml

from data_utils import find_class_names, split_dataset


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
            data_yaml_path = split_dataset(extract_dir, split_dir, split)
        else:
            data_yaml_path = find_yaml_file(extract_dir)

        train_model(data_yaml_path, model_size, epochs, img_size, batch_size, device)


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
