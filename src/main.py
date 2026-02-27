import os
import sys
from typing import Annotated, Optional

import typer

from annotate import annotate
from converter import convert
from cvat import cvat_app
from data_utils import data_app
from train import train
from utils import CONTEXT_SETTINGS

app = typer.Typer(
    help="Cvat auto annotation helper.", context_settings=CONTEXT_SETTINGS
)

app.command(name="annotate")(annotate)
app.command(name="convert")(convert)
app.add_typer(cvat_app, name="cvat")
app.command(name="train")(train)
app.add_typer(data_app, name="data")


@app.callback()
def global_options(
    stdout: Annotated[
        bool,
        typer.Option(
            "--stdout",
            help="Suppress all messages except the final output path to stdout.",
        ),
    ] = False,
):
    if stdout:
        sys.stderr = open(os.devnull, "w")


def main():
    app()


if __name__ == "__main__":
    main()
