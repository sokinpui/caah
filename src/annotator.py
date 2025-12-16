import argparse
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml

# Use the official SDK for online interaction
from cvat_sdk import make_client
from cvat_sdk.api_client import models
from cvat_sdk.core.helpers import TqdmProgressReporter
from dotenv import load_dotenv

from yolo_model import YoloModel


def add_annotate_arguments(parser):
    """Adds arguments for the annotate command."""
    parser.add_argument(
        "-m",
        "--model",
        required=True,
        help="Path to the YOLO model file (.pt).",
    )
    parser.add_argument(
        "-d",
        "--dataset",
        help="Path to the input dataset zip file (YOLO 1.1 format). Required for offline mode.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path for the output dataset zip file. Required for offline mode.",
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
    parser.add_argument(
        "--task-id",
        type=int,
        help="CVAT Task ID for online annotation (bypasses zip dataset).",
    )
    # --image-dir is no longer needed for online mode with SDK
    parser.add_argument(
        "--image-dir",
        type=Path,
        help="Local directory where task images are stored (only used for verification, optional).",
    )


def _xyxy_to_yolo(box, img_w, img_h):
    """
    Converts bounding box from [x1, y1, x2, y2] to [x_center, y_center, w, h] normalized.
    """
    x1, y1, x2, y2 = box

    w = x2 - x1
    h = y2 - y1
    x_center = x1 + (w / 2)
    y_center = y1 + (h / 2)

    x_center /= img_w
    y_center /= img_h
    w /= img_w
    h /= img_h

    x_center = max(0.0, min(1.0, x_center))
    y_center = max(0.0, min(1.0, y_center))
    w = max(0.0, min(1.0, w))
    h = max(0.0, min(1.0, h))

    return x_center, y_center, w, h


def _get_target_label_path(image_path: Path):
    """
    Determines the target path for the label file.
    Returns (path, exists_flag).
    """
    same_dir = image_path.with_suffix(".txt")
    if same_dir.exists():
        return same_dir, True

    parts = list(image_path.parts)
    if "images" in parts:
        idx = len(parts) - 1 - parts[::-1].index("images")
        parts[idx] = "labels"
        yolo_path = Path(*parts).with_suffix(".txt")

        if yolo_path.exists():
            return yolo_path, True
        if yolo_path.parent.exists():
            return yolo_path, False

    return same_dir, False


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

            # Using tqdm reporter for progress bar if available in env, else manual
            for frame_id in range(task.size):
                # Download frame to a temp file
                # The SDK retrieves the frame as a io.BytesIO object usually
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


def run_annotate(args):
    """
    Main execution flow for auto-annotation.
    """
    load_dotenv()

    model_path = Path(args.model)

    if not model_path.exists():
        print(f"Error: Model file not found at {model_path}", file=sys.stderr)
        sys.exit(1)

    # Initialize model
    try:
        model = YoloModel(str(model_path), device=args.device)
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        sys.exit(1)

    if args.task_id:
        # Online mode - no longer requires image_dir
        run_online(args, model)
        return

    # Offline mode checks
    if not args.dataset or not args.output:
        print(
            "Error: --dataset and --output are required for offline mode.",
            file=sys.stderr,
        )
        sys.exit(1)

    input_zip = Path(args.dataset)
    output_zip = Path(args.output)

    if not input_zip.exists():
        print(f"Error: Input dataset not found at {input_zip}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        dataset_dir = tmpdir_path / "dataset"
        dataset_dir.mkdir()

        print(f"Extracting {input_zip.name}...", file=sys.stderr)
        with zipfile.ZipFile(input_zip, "r") as zip_ref:
            zip_ref.extractall(dataset_dir)

        # Find images
        image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        image_files = [
            p for p in dataset_dir.rglob("*") if p.suffix.lower() in image_extensions
        ]

        if not image_files:
            print("No images found in the dataset.", file=sys.stderr)
            sys.exit(1)

        print(
            f"Found {len(image_files)} images. Starting annotation...", file=sys.stderr
        )

        # Handle class names and mapping
        existing_yaml = list(dataset_dir.rglob("data.yaml"))
        yaml_content = {"train": "images/train", "val": "images/val", "names": {}}

        if existing_yaml:
            try:
                with open(existing_yaml[0], "r") as f:
                    loaded = yaml.safe_load(f)
                    if loaded:
                        yaml_content.update(loaded)
            except Exception:
                pass
            yaml_path = existing_yaml[0]
        else:
            yaml_path = dataset_dir / "data.yaml"

        current_names = yaml_content.get("names", [])
        if isinstance(current_names, dict):
            current_names = [current_names[i] for i in sorted(current_names.keys())]

        if not current_names:
            current_names = list(model.model.names.values())

        model_names = model.model.names

        processed_count = 0

        for img_path in image_files:
            label_path, exists = _get_target_label_path(img_path)
            img_w, img_h = model.get_image_size(img_path)
            predictions = model.predict(img_path)

            label_lines = []
            for pred in predictions:
                class_id = pred["class_id"]
                class_name = model_names[class_id]
                box = pred["box"]

                target_class_id = class_id

                if args.mark_auto:
                    auto_name = f"{class_name} (auto)"
                    if auto_name not in current_names:
                        current_names.append(auto_name)
                    target_class_id = current_names.index(auto_name)
                else:
                    if class_name not in current_names:
                        current_names.append(class_name)
                    target_class_id = current_names.index(class_name)

                xc, yc, w, h = _xyxy_to_yolo(box, img_w, img_h)
                label_lines.append(
                    f"{target_class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}"
                )

            final_lines = []
            if exists:
                with open(label_path, "r") as f:
                    final_lines = [l.strip() for l in f.readlines() if l.strip()]

            final_lines.extend(label_lines)

            with open(label_path, "w") as f:
                f.write("\n".join(final_lines))

            processed_count += 1
            if processed_count % 10 == 0:
                print(
                    f"Processed {processed_count}/{len(image_files)}...",
                    end="\r",
                    file=sys.stderr,
                )

        print(f"\nProcessed {processed_count} images.", file=sys.stderr)

        print("Updating data.yaml...", file=sys.stderr)
        yaml_content["names"] = current_names
        yaml_content["nc"] = len(current_names)

        with open(yaml_path, "w") as f:
            yaml.dump(yaml_content, f, sort_keys=False)

        print(f"Zipping output to {output_zip}...", file=sys.stderr)
        output_base = str(output_zip.with_suffix(""))
        final_path = shutil.make_archive(output_base, "zip", dataset_dir)

        print(f"Done. Saved to {final_path}", file=sys.stderr)
        print(final_path)
