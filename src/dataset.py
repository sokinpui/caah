import os
from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv

from converter import coco_to_yolo, slice_coco_dataset, yolo_to_coco
from utils import CONTEXT_SETTINGS

dataset_app = typer.Typer(
    help="Dataset management utilities.", context_settings=CONTEXT_SETTINGS
)


@dataset_app.command("yolo2coco")
def yolo2coco(
    input_dir: Annotated[Path, typer.Argument(help="Input YOLO directory.")],
    output_dir: Annotated[Path, typer.Argument(help="Output COCO directory.")],
):
    """
    Converts a dataset from YOLO to COCO format.
    """
    nas_path_str = os.getenv("NAS_PATH")
    nas_prefix = os.getenv("NAS_PREFIX", "")

    yolo_to_coco(
        input_dir,
        output_dir,
        nas_path=Path(nas_path_str) if nas_path_str else None,
        nas_prefix=nas_prefix,
    )
    print(output_dir)


@dataset_app.command("slice")
def slice_dataset(
    input_dir: Annotated[Path, typer.Argument(help="Input COCO directory.")],
    output_dir: Annotated[Path, typer.Argument(help="Output sliced COCO directory.")],
    size: Annotated[
        str, typer.Option("--size", help="Slice size as H:W (pixels).")
    ] = "640:640",
    overlap: Annotated[
        str, typer.Option("--overlap", help="Overlap ratio as H:W (0.0-1.0).")
    ] = "0.2:0.2",
    jobs: Annotated[
        int, typer.Option("--jobs", "-j", help="Number of parallel slicing jobs.")
    ] = 4,
    nas: Annotated[
        bool,
        typer.Option(
            "--nas", help="Enable NAS optimization (requires NAS_PATH in .env)."
        ),
    ] = False,
):
    """
    Slices/Tiles a COCO dataset into smaller patches.
    """
    sh, sw = map(int, size.split(":"))
    oh, ow = map(float, overlap.split(":"))

    nas_path_str = os.getenv("NAS_PATH") if nas else None
    nas_prefix = os.getenv("NAS_PREFIX", "")

    if nas and not nas_path_str:
        raise ValueError("--nas requires NAS_PATH in .env")

    slice_coco_dataset(
        input_dir,
        output_dir,
        (sh, sw),
        (oh, ow),
        jobs,
        nas_path=Path(nas_path_str) if nas_path_str else None,
        nas_prefix=nas_prefix,
    )

    print(output_dir)


@dataset_app.command("coco2yolo")
def coco2yolo(
    input_dir: Annotated[Path, typer.Argument(help="Input COCO directory.")],
    output_dir: Annotated[Path, typer.Argument(help="Output YOLO directory.")],
):
    """
    Converts a dataset from COCO to YOLO format.
    """
    coco_to_yolo(input_dir, output_dir)
    print(output_dir)
