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


@dataset_app.command("convert")
def convert(
    input_file: Annotated[Path, typer.Argument(help="Input YOLO .zip file.")],
    output_file: Annotated[Path, typer.Argument(help="Output COCO .zip file.")],
):
    """
    Converts a dataset from YOLO to COCO format.
    """
    load_dotenv()
    nas_path_str = os.getenv("NAS_PATH")
    nas_prefix = os.getenv("NAS_PREFIX", "")

    yolo_to_coco(
        input_file,
        output_file,
        nas_path=Path(nas_path_str) if nas_path_str else None,
        nas_prefix=nas_prefix,
    )
    print(output_file)


@dataset_app.command("slice")
def slice_dataset(
    input_file: Annotated[Path, typer.Argument(help="Input COCO .zip file.")],
    output_file: Annotated[Path, typer.Argument(help="Output sliced COCO .zip file.")],
    size: Annotated[
        str, typer.Option("--size", help="Slice size as H:W (pixels).")
    ] = "640:640",
    overlap: Annotated[
        str, typer.Option("--overlap", help="Overlap ratio as H:W (0.0-1.0).")
    ] = "0.2:0.2",
):
    """
    Slices/Tiles a COCO dataset into smaller patches.
    """
    sh, sw = map(int, size.split(":"))
    oh, ow = map(float, overlap.split(":"))

    slice_coco_dataset(input_file, output_file, (sh, sw), (oh, ow))

    print(output_file)


@dataset_app.command("coco2yolo")
def coco2yolo(
    input_file: Annotated[Path, typer.Argument(help="Input COCO .zip file.")],
    output_file: Annotated[Path, typer.Argument(help="Output YOLO .zip file.")],
):
    """
    Converts a dataset from COCO to YOLO format.
    """
    coco_to_yolo(input_file, output_file)
    print(output_file)
