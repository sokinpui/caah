import argparse
import sys
import os
import argcomplete

from annotator import (
    add_annotate_online_arguments,
    run_annotate_online,
)
from cvat import run_cvat, setup_cvat_parser
from converter import add_convert_arguments, run_convert
from data_utils import setup_data_parser
from train import add_train_arguments, run_train


def main():
    """
    Main entry point for the command-line interface.
    """
    parser = argparse.ArgumentParser(description="Cvat auto annotation helper.")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Suppress all messages except the final output path to stdout.",
    )

    annotate_online_parser = subparsers.add_parser(
        "annotate-online", help="Run online auto-annotation."
    )
    add_annotate_online_arguments(annotate_online_parser)
    annotate_online_parser.set_defaults(func=run_annotate_online)

    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert dataset format locally.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    add_convert_arguments(convert_parser)
    convert_parser.set_defaults(func=run_convert)

    cvat_parser = subparsers.add_parser("cvat", help="Interact with a CVAT instance.")
    setup_cvat_parser(cvat_parser)
    cvat_parser.set_defaults(func=run_cvat)

    train_parser = subparsers.add_parser("train", help="Train a YOLO model.")
    add_train_arguments(train_parser)
    train_parser.set_defaults(func=run_train)

    data_parser = subparsers.add_parser("data", help="Dataset utilities.")
    setup_data_parser(data_parser)

    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    sys.stderr = open(os.devnull, "w") if args.stdout else sys.stderr

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
