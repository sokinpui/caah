import argparse
import sys
import tempfile
import zipfile
from pathlib import Path

import datumaro as dm


def add_convert_arguments(parser):
    """Adds convert-specific arguments to the parser."""
    parser.add_argument(
        "-i", "--input-file", required=True, help="Path to input dataset zip file."
    )
    parser.add_argument(
        "-o",
        "--output-file",
        required=True,
        help="Path for the output dataset zip file.",
    )
    parser.add_argument(
        "-f",
        "--from",
        dest="from_format",
        required=True,
        help=(
            "Input dataset format. Common formats include: "
            "\n- CVAT"
            "\n- YOLO"
            "\n- COCO (image_info, instances, person_keypoints, captions, labels)"
            "\n- PASCAL VOC (classification, detection, segmentation, action_classification, person_layout)"
            "\n- TF Detection API"
            "\n- WIDER Face"
            "\n- ImageNet, LabelMe, Roboflow, Cityscapes"
            "\n- MOT sequences, MOTS PNG, CamVid, ICDAR13/15, Market-1501, LFW. "
            "For a full list, refer to Datumaro documentation."
        ),
    )
    parser.add_argument(
        "-t",
        "--to",
        dest="to_format",
        required=True,
        help=(
            "Output dataset format. Common formats include: "
            "\n- CVAT"
            "\n- YOLO"
            "\n- COCO (image_info, instances, person_keypoints, captions, labels)"
            "\n- PASCAL VOC (classification, detection, segmentation, action_classification, person_layout)"
            "\n- TF Detection API"
            "\n- WIDER Face"
            "\n- ImageNet, LabelMe, Roboflow, Cityscapes"
            "\n- MOT sequences, MOTS PNG, CamVid, ICDAR13/15, Market-1501, LFW. "
            "For a full list, refer to Datumaro documentation."
        ),
    )


def run_convert(args):
    """Converts a dataset from one format to another using Datumaro."""
    input_zip = Path(args.input_file)
    output_zip = Path(args.output_file)

    if not input_zip.is_file():
        print(f"Error: Input file not found at {input_zip}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        input_dir = tmpdir_path / "input"
        output_dir = tmpdir_path / "output"
        input_dir.mkdir()
        output_dir.mkdir()

        print(f"Extracting {input_zip} to temporary directory...", file=sys.stderr)
        with zipfile.ZipFile(input_zip, "r") as zip_ref:
            zip_ref.extractall(input_dir)

        print(
            f"Importing dataset from {input_dir} (format: {args.from_format})...",
            file=sys.stderr,
        )
        try:
            dataset = dm.Dataset.import_from(
                str(input_dir), format=args.from_format.lower()
            )
        except Exception as e:
            print(f"Error importing dataset: {e}", file=sys.stderr)
            print(
                "Files in extracted directory:",
                [str(p.relative_to(input_dir)) for p in input_dir.rglob("*")],
                file=sys.stderr,
            )
            sys.exit(1)

        print(
            f"Exporting dataset to {output_dir} (format: {args.to_format.lower()})...",
            file=sys.stderr,
        )
        dataset.export(str(output_dir), format=args.to_format.lower(), save_media=True)

        print(f"Creating output zip file at {output_zip}...", file=sys.stderr)
        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for entry in output_dir.rglob("*"):
                zipf.write(entry, entry.relative_to(output_dir))

    print(output_zip)


def main():
    """Main function to run the converter script directly."""
    parser = argparse.ArgumentParser(
        description="Convert dataset format locally.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    add_convert_arguments(parser)
    args = parser.parse_args()
    run_convert(args)


if __name__ == "__main__":
    main()
