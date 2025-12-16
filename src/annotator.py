import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from annotate_offline import run_offline
from annotate_online import run_online
from yolo_model import YoloModel


def _load_yolo_model(model_path_str: str, device: str) -> YoloModel:
    """Loads a YOLO model, handling errors."""
    model_path = Path(model_path_str)
    if not model_path.exists():
        print(f"Error: Model file not found at {model_path}", file=sys.stderr)
        sys.exit(1)
    try:
        return YoloModel(str(model_path), device=device)
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        sys.exit(1)


def add_annotate_offline_arguments(parser):
    """Adds arguments for the annotate-offline command."""
    parser.add_argument(
        "-m",
        "--model",
        required=True,
        help="Path to the YOLO model file (.pt).",
    )
    parser.add_argument(
        "-d",
        "--dataset",
        required=True,
        help="Path to the input dataset zip file (YOLO 1.1 format).",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Path for the output dataset zip file.",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help="Device to run inference on (cpu, gpu). Default: cpu",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold for predictions. Default: 0.25",
    )
    parser.add_argument(
        "--no-mark-auto",
        dest="mark_auto",
        action="store_false",
        help="Disable appending ' (auto)' to class names for generated annotations.",
    )
    parser.set_defaults(mark_auto=True)


def run_annotate_offline(args):
    """Main execution flow for offline auto-annotation."""
    load_dotenv()
    model = _load_yolo_model(args.model, args.device)
    run_offline(args, model)


def add_annotate_online_arguments(parser):
    """Adds arguments for the annotate-online command."""
    parser.add_argument(
        "-m", "--model", required=True, help="Path to the YOLO model file (.pt)."
    )
    parser.add_argument(
        "--task-id",
        type=int,
        required=True,
        help="CVAT Task ID for online annotation.",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help="Device to run inference on (cpu, gpu). Default: cpu",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold for predictions. Default: 0.25",
    )


def run_annotate_online(args):
    """Main execution flow for online auto-annotation."""
    load_dotenv()
    model = _load_yolo_model(args.model, args.device)
    run_online(args, model)
