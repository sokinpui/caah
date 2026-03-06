import logging
import os
import sys
from typing import Annotated, Optional

import typer

from annotate import annotate
from cvat import cvat_app
from dataset import dataset_app
from migrate import migrate_app
from train import train
from utils import CONTEXT_SETTINGS, setup_logging

# Suppress CVAT SDK version compatibility warnings
logging.getLogger("cvat_sdk").setLevel(logging.ERROR)

setup_logging()

app = typer.Typer(
    help="CVAT auto annotation helper.", context_settings=CONTEXT_SETTINGS
)

app.command(name="annotate")(annotate)
app.add_typer(cvat_app, name="cvat")
app.add_typer(dataset_app, name="dataset")
app.add_typer(migrate_app, name="migrate")
app.command(name="train")(train)


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
