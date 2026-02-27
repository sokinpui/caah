import os
import sys
from typing import Annotated, Optional

import typer

from annotate import annotate
from cvat import cvat_app
from train import train
from utils import CONTEXT_SETTINGS

app = typer.Typer(
    help="Cvat auto annotation helper.", context_settings=CONTEXT_SETTINGS
)

app.command(name="annotate")(annotate)
app.add_typer(cvat_app, name="cvat")
app.command(name="train")(train)


@app.command()
def server(
    host: str = "0.0.0.0",
    port: int = 8000,
):
    """Start the REST API server."""
    import uvicorn

    uvicorn.run("server:app", host=host, port=port, reload=True)


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
