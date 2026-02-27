import io
import os
import sys
from pathlib import Path

from cvat_sdk import make_client
from cvat_sdk.api_client import models
from dotenv import load_dotenv
from PIL import Image

from yolo_model import YoloModel


def add_annotate_arguments(parser):
    """Adds arguments for the annotate command."""
    parser.add_argument(
        "-m", "--model", required=True, help="Path to the YOLO model file (.pt)."
    )
    parser.add_argument(
        "--task-id",
        type=int,
        required=True,
        help="CVAT Task ID for annotation.",
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


def run_annotate_task(args):
    """Main execution flow for auto-annotation."""
    load_dotenv()
    model = _load_yolo_model(args.model, args.device)

    url = os.getenv("CVAT_URL")
    user = os.getenv("CVAT_USERNAME")
    password = os.getenv("CVAT_PASSWORD")

    if not all([url, user, password]):
        print(
            "Error: CVAT credentials not found in environment variables.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Connecting to CVAT at {url}...", file=sys.stderr)

    with make_client(url, credentials=(user, password)) as client:
        print(f"Fetching task {args.task_id}...", file=sys.stderr)
        task = client.tasks.retrieve(args.task_id)

        labels = task.get_labels()
        label_map = {l.name: l.id for l in labels}
        source_attr_map = {
            label.id: attr.id
            for label in labels
            for attr in label.attributes
            if attr.name == "source"
        }

        print(f"Task has {task.size} frames. Starting inference...", file=sys.stderr)

        shapes_buffer = []
        BATCH_SIZE = 100

        for frame_id in range(task.size):
            image_bytes = task.get_frame(frame_id).read()
            image_source = Image.open(io.BytesIO(image_bytes))
            predictions = model.predict(image_source)

            for pred in predictions:
                class_name = pred["label"]
                if class_name not in label_map:
                    continue

                l_id = label_map[class_name]
                attributes = []
                if l_id in source_attr_map:
                    attributes.append(
                        models.AttributeValRequest(
                            spec_id=source_attr_map[l_id], value="auto"
                        )
                    )

                shapes_buffer.append(
                    models.LabeledShapeRequest(
                        type=models.ShapeType("rectangle"),
                        frame=frame_id,
                        label_id=l_id,
                        points=pred["box"],
                        rotation=0,
                        attributes=attributes,
                        source="auto",
                    )
                )

            if len(shapes_buffer) >= BATCH_SIZE:
                print(
                    f"Uploading batch of {len(shapes_buffer)} annotations...",
                    end="\r",
                    file=sys.stderr,
                )
                task.update_annotations(
                    models.PatchedLabeledDataRequest(shapes=shapes_buffer)
                )
                shapes_buffer = []

            print(
                f"Processed frame {frame_id+1}/{task.size}...",
                end="\r",
                file=sys.stderr,
            )

        if shapes_buffer:
            task.update_annotations(
                models.PatchedLabeledDataRequest(shapes=shapes_buffer)
            )

    print(f"\nDone. Annotated task {args.task_id}.", file=sys.stderr)


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
