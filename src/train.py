import importlib.util
import os
import tempfile
from pathlib import Path
from typing import Annotated, Optional

import typer
from dotenv import load_dotenv

from data_utils import split_dataset
from utils import extract_zip, find_file, resolve_device


def train_model(
    data_yaml_path: Path,
    model_spec: str,
    epochs: int,
    img_size: int,
    batch_size: int,
    device: str,
    nas_path: Optional[str] = None,
    save_period: int = -1,
    workers: int = 8,
    project: Optional[str] = None,
    name: Optional[str] = None,
    augmentations: Optional[list] = None,
):
    """Initializes and trains the YOLO model."""
    print("--- Starting Training ---")
    from ultralytics import YOLO

    resolved_device = resolve_device(device)

    print(f"Data: {data_yaml_path}")
    print(f"Model: {model_spec}")
    print(f"Epochs: {epochs}")

    model = YOLO(model_spec)

    results = model.train(
        data=str(data_yaml_path),
        epochs=epochs,
        imgsz=img_size,
        batch=batch_size,
        device=resolved_device,
        cache=nas_path is not None,
        plots=True,
        save=True,
        save_period=save_period,
        workers=workers,
        project=project,
        name=name,
        augmentations=augmentations,
    )

    print("--- Training Complete ---")
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
    nas_prefix: str = "",
    save_period: int = -1,
    workers: int = 8,
    project: Optional[str] = None,
    name: Optional[str] = None,
    augmentations: Optional[list] = None,
):
    """Extracts the dataset from a zip file and initiates the training process."""
    zip_path = Path(dataset_zip_path)
    if not zip_path.is_file() or zip_path.suffix.lower() != ".zip":
        raise FileNotFoundError(
            f"Dataset path is not a valid zip file: {dataset_zip_path}"
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        extract_dir = tmpdir_path / "extracted"
        extract_dir.mkdir()

        print(f"Extracting dataset to temporary directory: {extract_dir}")
        extract_zip(zip_path, extract_dir)

        if split:
            print(f"Splitting dataset with ratio {split}...")
            split_dir = tmpdir_path / "split"
            split_dir.mkdir()
            data_yaml_path = split_dataset(
                extract_dir, split_dir, split, nas_path=nas_path, nas_prefix=nas_prefix
            )
        else:
            data_yaml_path = find_file(extract_dir, ["data.yaml"])

        if not data_yaml_path:
            raise FileNotFoundError(f"Could not find 'data.yaml' in {extract_dir}")

        train_model(
            data_yaml_path,
            model_spec,
            epochs,
            img_size,
            batch_size,
            device,
            nas_path=nas_path,
            save_period=save_period,
            workers=workers,
            project=project,
            name=name,
            augmentations=augmentations,
        )


def _load_custom_augmentations(file_path: Path) -> list:
    """Dynamically loads 'custom_transforms' from a python file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Augmentation file not found: {file_path}")

    spec = importlib.util.spec_from_file_location("custom_aug", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load python spec for {file_path}")

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        raise RuntimeError(f"Error executing augmentation file: {e}")

    if not hasattr(module, "custom_transforms"):
        raise AttributeError(
            f"The file {file_path} must define a variable named 'custom_transforms'"
        )

    print(f"Loaded custom augmentations from {file_path}")
    return getattr(module, "custom_transforms")


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
    project: Annotated[
        Optional[str], typer.Option("--project", help="Project name.")
    ] = None,
    name: Annotated[
        Optional[str], typer.Option("--name", help="Experiment name.")
    ] = None,
    save_period: Annotated[
        int, typer.Option("--save-period", help="Save checkpoint every x epochs.")
    ] = -1,
    workers: Annotated[
        int, typer.Option("--workers", help="Number of data loader workers.")
    ] = 8,
    augmentation: Annotated[
        Optional[Path],
        typer.Option(
            "--augmentation", "-a", help="Path to .py file defining custom_transforms."
        ),
    ] = None,
    network_drive: bool = False,
):
    """Main entry point for the training command."""
    load_dotenv()

    model_spec = path if path else model
    if not model_spec.endswith(".pt"):
        model_spec += ".pt"

    nas_path = os.getenv("NAS_PATH") if network_drive else None
    nas_prefix = os.getenv("NAS_PREFIX", "")

    if network_drive and not nas_path:
        raise ValueError("--network-drive requires NAS_PATH in .env")

    custom_aug = None
    if augmentation:
        custom_aug = _load_custom_augmentations(augmentation)

    process_dataset_and_train(
        dataset_zip_path=data,
        model_spec=model_spec,
        epochs=epochs,
        img_size=imgsz,
        batch_size=batch,
        device=device,
        split=split,
        nas_path=nas_path,
        nas_prefix=nas_prefix,
        save_period=save_period,
        workers=workers,
        project=project,
        name=name,
        augmentations=custom_aug,
    )
