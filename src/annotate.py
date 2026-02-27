import io
import os
from pathlib import Path
from typing import Annotated

import typer
from cvat_sdk import make_client
from cvat_sdk.api_client import models
from dotenv import load_dotenv
from PIL import Image

from yolo_model import YoloModel


def annotate(
    model_path: Annotated[
        Path, typer.Option("--model", "-m", help="Path to YOLO model file (.pt).")
    ],
    task_id: Annotated[int, typer.Option("--task-id", help="CVAT Task ID.")],
    device: Annotated[str, typer.Option(help="Device (cpu, gpu).")] = "cpu",
    conf: Annotated[float, typer.Option(help="Confidence threshold.")] = 0.25,
) -> None:
    """Main execution flow for auto-annotation."""
    load_dotenv()
    model = _load_yolo_model(str(model_path), device)

    url, user, password = (
        os.getenv("CVAT_URL"),
        os.getenv("CVAT_USERNAME"),
        os.getenv("CVAT_PASSWORD"),
    )
    if not all([url, user, password]):
        raise ValueError("CVAT credentials not found in environment variables.")

    print(f"Connecting to CVAT at {url}...")

    with make_client(url, credentials=(user, password)) as client:
        print(f"Fetching task {task_id}...")
        task = client.tasks.retrieve(task_id)

        labels = task.get_labels()
        label_map = {l.name: l.id for l in labels}
        source_attr_map = {
            label.id: attr.id
            for label in labels
            for attr in label.attributes
            if attr.name == "source"
        }

        print(f"Task has {task.size} frames. Starting inference...")

        shapes_buffer = []

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

            print(
                f"Processed frame {frame_id+1}/{task.size}...",
                end="\r",
            )

        if shapes_buffer:
            task.update_annotations(
                models.PatchedLabeledDataRequest(shapes=shapes_buffer)
            )

    print(f"\nDone. Annotated task {task_id}.")


def _load_yolo_model(model_path_str: str, device: str) -> YoloModel:
    """Loads a YOLO model, handling errors."""
    model_path = Path(model_path_str)
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")

    try:
        return YoloModel(str(model_path), device=device)
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")
