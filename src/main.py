import argparse
import sys
from pathlib import Path

# Add src to path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from annotator import AutoAnnotator, UnsupportedFormatException, get_formatter


def main():
    """
    Main function to run the auto-annotation process.
    It parses command-line arguments, initializes the annotator and formatter,
    and processes the images.
    """
    parser = argparse.ArgumentParser(
        description="Auto-annotate images using a trained model."
    )
    parser.add_argument(
        "-m", "--model", type=str, required=True, help="Path to the trained model."
    )
    parser.add_argument(
        "-i",
        "--images",
        type=str,
        required=True,
        help="Path to the directory containing images.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Path to the directory to save annotations.",
    )
    parser.add_argument(
        "--output-format",
        type=str,
        default="cvat",
        choices=["cvat", "yolo"],
        help="Format for the output annotations.",
    )
    parser.add_argument(
        "-c",
        "--copy",
        action="store_true",
        help="Copy original images to the output directory.",
    )

    args = parser.parse_args()

    images_path = Path(args.images)
    if not images_path.is_dir():
        print(f"Error: Image directory not found at {args.images}")
        return

    try:
        annotator = AutoAnnotator(args.model)
        formatter = get_formatter(args.output_format)
        annotator.process_images(
            images_path, Path(args.output), formatter, copy_images=args.copy
        )
    except (FileNotFoundError, UnsupportedFormatException) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
