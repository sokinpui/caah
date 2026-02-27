import os
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Annotated, Optional

import typer
import yaml
from dotenv import load_dotenv

from data_utils import find_class_names, split_dataset
from utils import resolve_device


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
    model_spec: str,
    epochs: int,
    img_size: int,
    batch_size: int,
    device: str,
    nas_path: Optional[str] = None,
):
    """
    Initializes and trains the YOLO model.
    """
    print("--- Starting Training ---", file=sys.stderr)
    from ultralytics import YOLO

    resolved_device = resolve_device(device)

    print(f"Data: {data_yaml_path}", file=sys.stderr)
    print(f"Model: {model_spec}", file=sys.stderr)
    print(f"Epochs: {epochs}", file=sys.stderr)

    model = YOLO(model_spec)

    results = model.train(
        data=str(data_yaml_path),
        epochs=epochs,
        imgsz=img_size,
        batch=batch_size,
        device=resolved_device,
        cache=nas_path is not None,  # Recommendation: cache when using network drive
        plots=True,
        save=True,
    )

    print("--- Training Complete ---", file=sys.stderr)
    best_model_path = f"{results.save_dir}/weights/best.pt"
    print(best_model_path)


def process_dataset_and_train(
    dataset_zip_path: str,
    model_spec: str,
    epochs: int,
    img_size: int,
    batch_size: int,
    device: str,
    split: Optional[str] = None,
    nas_path: Optional[str] = None,
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
            data_yaml_path = split_dataset(
                extract_dir, split_dir, split, nas_path=nas_path
            )
        else:
            data_yaml_path = find_yaml_file(extract_dir)

        train_model(
            data_yaml_path,
            model_spec,
            epochs,
            img_size,
            batch_size,
            device,
            nas_path=nas_path,
        )


def train(
    data: Annotated[str, typer.Option("--data", "-d", help="Zipped dataset path.")],
    model: Annotated[
        str, typer.Option("--model", "-m", help="YOLO model version.")
    ] = "yolo11n",
    path: Annotated[
        Optional[str], typer.Option("--path", "-p", help="Custom model .pt path.")
    ] = None,
    epochs: Annotated[int, typer.Option("--epochs", "-e")] = 50,
    imgsz: int = 640,
    batch: Annotated[int, typer.Option("--batch", "-b")] = 16,
    device: str = "gpu",
    split: Annotated[Optional[str], typer.Option("--split", "-s")] = None,
    network_drive: bool = False,
):
    """
    Runs the training process with parsed arguments.
    """
    load_dotenv()
    try:
        model_spec = path if path else model
        if not model_spec.endswith(".pt"):
            model_spec += ".pt"

        nas_path = None
        if network_drive:
            nas_path = os.getenv("NAS_PATH")

        if network_drive and not nas_path:
            print("Error: --network-drive requires NAS_PATH in .env", file=sys.stderr)
            sys.exit(1)

        process_dataset_and_train(
            dataset_zip_path=data,
            model_spec=model_spec,
            epochs=epochs,
            img_size=imgsz,
            batch_size=batch,
            device=device,
            split=split,
            nas_path=nas_path,
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
