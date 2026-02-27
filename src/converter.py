import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Annotated

import datumaro as dm
import typer


def convert(
    input_file: Annotated[
        Path, typer.Option("--input-file", "-i", help="Input dataset zip.")
    ],
    output_file: Annotated[
        Path, typer.Option("--output-file", "-o", help="Output dataset zip.")
    ],
    from_format: Annotated[
        str, typer.Option("--from", "-f", help="Source format (e.g., cvat, yolo).")
    ],
    to_format: Annotated[str, typer.Option("--to", "-t", help="Target format.")],
):
    """Converts a dataset from one format to another using Datumaro."""
    if not input_file.is_file():
        print(f"Error: Input file not found at {input_file}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        input_dir = tmpdir_path / "input"
        output_dir = tmpdir_path / "output"
        input_dir.mkdir()
        output_dir.mkdir()

        print(f"Extracting {input_file} to temporary directory...", file=sys.stderr)
        with zipfile.ZipFile(input_file, "r") as zip_ref:
            zip_ref.extractall(input_dir)

        print(
            f"Importing dataset from {input_dir} (format: {from_format})...",
            file=sys.stderr,
        )
        try:
            dataset = dm.Dataset.import_from(str(input_dir), format=from_format.lower())
        except Exception as e:
            print(f"Error importing dataset: {e}", file=sys.stderr)
            print(
                "Files in extracted directory:",
                [str(p.relative_to(input_dir)) for p in input_dir.rglob("*")],
                file=sys.stderr,
            )
            sys.exit(1)

        print(
            f"Exporting dataset to {output_dir} (format: {to_format.lower()})...",
            file=sys.stderr,
        )
        dataset.export(str(output_dir), format=to_format.lower(), save_media=True)

        print(f"Creating output zip file at {output_file}...", file=sys.stderr)
        with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for entry in output_dir.rglob("*"):
                zipf.write(entry, entry.relative_to(output_dir))

    print(output_file)
