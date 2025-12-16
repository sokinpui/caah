import os
import sys
import tempfile
from pathlib import Path

from cvat_sdk import make_client
from cvat_sdk.api_client import models
from dotenv import load_dotenv

from yolo_model import YoloModel


def run_online(args, model):
    """
    Execution flow for online auto-annotation using official CVAT SDK.
    Downloads frames on-the-fly, infers, and uploads annotations.
    """
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

        # 1. Map Labels
        # We need to map YOLO class names (strings) to CVAT Label IDs (integers)
        # and identify the 'source' attribute ID if it exists.
        labels = task.get_labels()
        label_map = {l.name: l.id for l in labels}
        source_attr_map = {}

        for label in labels:
            for attr in label.attributes:
                if attr.name == "source":
                    source_attr_map[label.id] = attr.id
                    break

        print(f"Task has {task.size} frames. Starting inference...", file=sys.stderr)

        shapes_buffer = []
        BATCH_SIZE = 100

        # 2. Iterate over frames
        # We use a temp directory to store the downloaded frame for YOLO to read
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            for frame_id in range(task.size):
                # Download frame to a temp file
                frame_data = task.get_frame(frame_id)

                # Determine extension based on mime_type or default to jpg
                ext = ".jpg"
                temp_img_path = tmp_path / f"frame_{frame_id}{ext}"

                with open(temp_img_path, "wb") as f:
                    f.write(frame_data.read())

                # Run Inference
                predictions = model.predict(temp_img_path)

                # Process Predictions
                for pred in predictions:
                    class_name = pred["label"]
                    box = pred["box"]  # [x1, y1, x2, y2]

                    if class_name not in label_map:
                        # Warning: Model predicts a class not in CVAT task
                        continue

                    l_id = label_map[class_name]

                    # Handle Attributes (e.g., auto tag)
                    attributes = []
                    if l_id in source_attr_map:
                        attributes.append(
                            models.AttributeValRequest(
                                spec_id=source_attr_map[l_id], value="auto"
                            )
                        )

                    # Create Shape
                    # Points in CVAT are [x1, y1, x2, y2] for rectangle
                    shape = models.LabeledShapeRequest(
                        type=models.ShapeType("rectangle"),
                        frame=frame_id,
                        label_id=l_id,
                        points=box,
                        rotation=0,
                        attributes=attributes,
                        source="auto",  # Mark the annotation itself as auto generated
                    )
                    shapes_buffer.append(shape)

                os.remove(temp_img_path)

                # Batch Upload
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

            # Upload remaining
            if shapes_buffer:
                task.update_annotations(
                    models.PatchedLabeledDataRequest(shapes=shapes_buffer)
                )

    print(f"\nDone. Annotated task {args.task_id}.", file=sys.stderr)
