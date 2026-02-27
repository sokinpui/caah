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
    ioa: Annotated[
        float, typer.Option(help="IoA threshold to drop old annotations.")
    ] = 0.5,
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
        all_annotations = task.get_annotations()

        labels = task.get_labels()
        label_map = {l.name: l.id for l in labels}
        source_attr_map = {
            label.id: attr.id
            for label in labels
            for attr in label.attributes
            if attr.name == "source"
        }

        print(f"Task has {task.size} frames. Starting inference...")

        new_shapes = []
        dropped_ids = set()

        for frame_id in range(task.size):
            frame_existing = [
                s
                for s in all_annotations.shapes
                if s.frame == frame_id and s.type.value == "rectangle"
            ]

            image_bytes = task.get_frame(frame_id).read()
            image_source = Image.open(io.BytesIO(image_bytes))
            predictions = model.predict(image_source)

            for pred in predictions:
                class_name = pred["label"]
                if class_name not in label_map:
                    continue

                for exist in frame_existing:
                    if _calculate_ioa(pred["box"], exist.points) <= ioa:
                        continue
                    
                    if exist.source.value != "manual":
                        dropped_ids.add(exist.id)

                l_id = label_map[class_name]
                attributes = []
                if l_id in source_attr_map:
                    attributes.append(
                        models.AttributeValRequest(
                            spec_id=source_attr_map[l_id], value="auto"
                        )
                    )

                new_shapes.append(
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

        kept_shapes = [
            models.LabeledShapeRequest(**s.to_dict())
            for s in all_annotations.shapes
            if s.id not in dropped_ids
        ]

        task.set_annotations(
            models.LabeledDataRequest(
                shapes=kept_shapes + new_shapes,
                tracks=[
                    models.LabeledTrackRequest(**t.to_dict())
                    for t in all_annotations.tracks
                ],
                tags=[
                    models.LabeledImageRequest(**t.to_dict())
                    for t in all_annotations.tags
                ],
            )
        )

    print(f"\nDone. Annotated task {task_id}.")


def _calculate_ioa(new_box: list[float], old_box: list[float]) -> float:
    """Calculate Intersection over Area (IoA) relative to the old box."""
    x_min, y_min = max(new_box[0], old_box[0]), max(new_box[1], old_box[1])
    x_max, y_max = min(new_box[2], old_box[2]), min(new_box[3], old_box[3])

    if x_max <= x_min or y_max <= y_min:
        return 0.0

    intersection_area = (x_max - x_min) * (y_max - y_min)
    old_area = (old_box[2] - old_box[0]) * (old_box[3] - old_box[1])

    return intersection_area / old_area if old_area > 0 else 0.0


def _load_yolo_model(model_path_str: str, device: str) -> YoloModel:
    """Loads a YOLO model, handling errors."""
    model_path = Path(model_path_str)
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")

    try:
        return YoloModel(str(model_path), device=device)
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")
