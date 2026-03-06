import os
from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv

from converter import yolo_to_coco
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
