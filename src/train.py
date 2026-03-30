import importlib.util
import os
import tempfile
from pathlib import Path
from typing import Annotated, Optional

import typer
from dotenv import load_dotenv

from data_utils import split_coco_dataset, split_dataset
from utils import find_file, resolve_device


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

    if results is None:
        return

    print(f"{results.save_dir}/weights/best.pt")


def prepare_and_train(
    dataset_path: str,
    model_spec: str,
    epochs: int,
    img_size: int,
    batch_size: int,
    device: str,
    format: str = "yolo",
    split: Optional[str] = None,
    nas_path: Optional[str] = None,
    nas_prefix: str = "",
    save_period: int = -1,
    workers: int = 8,
    project: Optional[str] = None,
    name: Optional[str] = None,
    augmentations: Optional[list] = None,
):
    dataset_root = Path(dataset_path)
    if not dataset_root.is_dir():
        raise NotADirectoryError(f"Dataset directory not found: {dataset_path}")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        if split and format == "yolo":
            print(f"Splitting dataset with ratio {split}...")
            split_dir = tmpdir_path / "split"
            split_dir.mkdir()
            data_yaml_path = split_dataset(
                dataset_root, split_dir, split, nas_path=nas_path, nas_prefix=nas_prefix
            )
        elif split and format == "coco":
            print(f"Splitting COCO dataset with ratio {split}...")
            split_dir = tmpdir_path / "split"
            split_dir.mkdir()
            data_yaml_path = split_coco_dataset(
                dataset_root, split_dir, split, nas_path=nas_path, nas_prefix=nas_prefix
            )
        else:
            data_yaml_path = find_file(dataset_root, ["data.yaml"])

        if not data_yaml_path:
            raise FileNotFoundError(f"Could not find 'data.yaml' in {dataset_path}")

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
    data: Annotated[str, typer.Option("--data", "-d", help="Dataset directory path.")],
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
    nas: Annotated[
        bool,
        typer.Option(
            "--nas", help="Enable NAS optimization (requires NAS_PATH in .env)."
        ),
    ] = False,
    format: Annotated[
        str,
        typer.Option("--format", help="Dataset format: 'yolo' or 'coco'."),
    ] = "yolo",
):
    """Main entry point for the training command."""
    load_dotenv()

    model_spec = path if path else model
    if not model_spec.endswith(".pt"):
        model_spec += ".pt"

    nas_path = os.getenv("NAS_PATH") if nas else None
    nas_prefix = os.getenv("NAS_PREFIX", "")

    if nas and not nas_path:
        raise ValueError("--network-drive requires NAS_PATH in .env")

    custom_aug = None
    if augmentation:
        custom_aug = _load_custom_augmentations(augmentation)

    prepare_and_train(
        dataset_path=data,
        model_spec=model_spec,
        epochs=epochs,
        img_size=imgsz,
        batch_size=batch,
        device=device,
        format=format.lower(),
        split=split,
        nas_path=nas_path,
        nas_prefix=nas_prefix,
        save_period=save_period,
        workers=workers,
        project=project,
        name=name,
        augmentations=custom_aug,
    )
