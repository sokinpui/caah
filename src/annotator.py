import argparse
import os
import sys
import shutil
import tempfile
import zipfile
import yaml
from pathlib import Path
from dotenv import load_dotenv

from cvat import CVATApi
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
    parser.add_argument(
        "--image-dir",
        type=Path,
        help="Local directory where task images are stored (required for online mode).",
    )


def _xyxy_to_yolo(box, img_w, img_h):
    """
    Converts bounding box from [x1, y1, x2, y2] to [x_center, y_center, w, h] normalized.
    """
    x1, y1, x2, y2 = box
    
    # Calculate center and width/height
    w = x2 - x1
    h = y2 - y1
    x_center = x1 + (w / 2)
    y_center = y1 + (h / 2)

    # Normalize
    x_center /= img_w
    y_center /= img_h
    w /= img_w
    h /= img_h

    # Clip values to ensure they are within [0, 1]
    x_center = max(0.0, min(1.0, x_center))
    y_center = max(0.0, min(1.0, y_center))
    w = max(0.0, min(1.0, w))
    h = max(0.0, min(1.0, h))

    return x_center, y_center, w, h


def _get_target_label_path(image_path: Path):
    """
    Determines the target path for the label file.
    Returns (path, exists_flag).
    Priority:
    1. Existing file in same directory.
    2. Existing file in 'labels' directory (mapped from 'images').
    3. New file in 'labels' directory (if parent exists).
    4. New file in same directory.
    """
    # 1. Check same directory
    same_dir = image_path.with_suffix(".txt")
    if same_dir.exists():
        return same_dir, True

    # 2. Check standard YOLO folder structure (images -> labels)
    parts = list(image_path.parts)
    # Iterate parts to find "images" (could be multiple, use the last one that makes sense)
    # A simple approach is finding the last occurrence of "images"
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
    Execution flow for online auto-annotation (CVAT API).
    """
    load_dotenv()
    url = os.getenv("CVAT_URL")
    user = os.getenv("CVAT_USERNAME")
    password = os.getenv("CVAT_PASSWORD")

    if not all([url, user, password]):
        print("Error: CVAT credentials not found in environment variables.", file=sys.stderr)
        sys.exit(1)

    api = CVATApi(url, user, password)
    task_id = args.task_id

    print(f"Fetching metadata for task {task_id}...", file=sys.stderr)
    labels = api.get_task_labels(task_id)
    data_meta = api.get_task_data_meta(task_id)

    label_map = {}
    source_attr_map = {}

    for label in labels:
        l_name = label["name"]
        l_id = label["id"]
        label_map[l_name] = l_id

        for attr in label.get("attributes", []):
            if attr["name"] == "source":
                if attr["input_type"] in ["select", "radio"]:
                    values = attr.get("values", [])
                    if "auto" not in values:
                        print(f"Warning: 'source' attribute for label '{l_name}' does not have 'auto' option.", file=sys.stderr)
                        continue
                source_attr_map[l_id] = attr["id"]
                break

    frames = data_meta.get("frames", [])
    if not frames:
        print("Error: No frame information found in task data.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(frames)} frames. Starting annotation...", file=sys.stderr)

    shapes_buffer = []
    processed_count = 0
    BATCH_SIZE = 100

    for i, frame_info in enumerate(frames):
        frame_idx = i
        file_name = frame_info.get("name")
        image_path = args.image_dir / file_name

        if not image_path.exists():
            print(f"Warning: Image not found at {image_path}. Skipping.", file=sys.stderr)
            continue

        predictions = model.predict(image_path)

        for pred in predictions:
            class_name = pred["label"]
            box = pred["box"]
            
            if class_name not in label_map:
                continue

            l_id = label_map[class_name]
            attributes = []
            if l_id in source_attr_map:
                attributes.append({"spec_id": source_attr_map[l_id], "value": "auto"})

            shape = {
                "type": "rectangle",
                "frame": frame_idx,
                "label_id": l_id,
                "points": box,
                "rotation": 0,
                "attributes": attributes,
            }
            shapes_buffer.append(shape)

        processed_count += 1
        print(f"Processed {processed_count}/{len(frames)}...", end="\r", file=sys.stderr)

        if len(shapes_buffer) >= BATCH_SIZE:
            api.patch_annotations(task_id, {"shapes": shapes_buffer, "version": 0})
            shapes_buffer = []

    if shapes_buffer:
        api.patch_annotations(task_id, {"shapes": shapes_buffer, "version": 0})
    
    print(f"\nDone. Processed {processed_count} frames.", file=sys.stderr)


def run_annotate(args):
    """
    Main execution flow for auto-annotation.
    """
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
        if not args.image_dir:
            print("Error: --image-dir is required when --task-id is provided.", file=sys.stderr)
            sys.exit(1)
        run_online(args, model)
        return

    if not args.dataset or not args.output:
        print("Error: --dataset and --output are required for offline mode.", file=sys.stderr)
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

        print(f"Found {len(image_files)} images. Starting annotation...", file=sys.stderr)

        # Handle class names and mapping
        existing_yaml = list(dataset_dir.rglob("data.yaml"))
        yaml_content = {"train": "images/train", "val": "images/val", "names": {}}
        
        # Load existing names if available
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

        # Ensure names is a dict or list, convert to list for processing
        current_names = yaml_content.get("names", [])
        if isinstance(current_names, dict):
            # handle {0: 'a', 1: 'b'}
            current_names = [current_names[i] for i in sorted(current_names.keys())]
        
        # If dataset was empty of names, use model names
        if not current_names:
            current_names = list(model.model.names.values())

        # Determine target class IDs
        model_names = model.model.names # dict {0: 'name'}
        
        processed_count = 0

        for img_path in image_files:
            # Determine label path
            label_path, exists = _get_target_label_path(img_path)

            # Get image dimensions
            img_w, img_h = model.get_image_size(img_path)
            
            # Predict
            predictions = model.predict(img_path)
            
            # Prepare label content
            label_lines = []
            for pred in predictions:
                class_id = pred["class_id"]
                class_name = model_names[class_id]
                box = pred["box"]
                
                target_class_id = class_id

                # Map to _auto class if requested
                if args.mark_auto:
                    auto_name = f"{class_name} (auto)"
                    if auto_name not in current_names:
                        current_names.append(auto_name)
                    target_class_id = current_names.index(auto_name)
                else:
                    # Ensure class exists in current_names
                    if class_name not in current_names:
                        current_names.append(class_name)
                    target_class_id = current_names.index(class_name)

                xc, yc, w, h = _xyxy_to_yolo(box, img_w, img_h)
                label_lines.append(f"{target_class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}")

            # Prepare final content (Append to existing if present)
            final_lines = []
            if exists:
                with open(label_path, "r") as f:
                    # Read existing lines and strip whitespace
                    final_lines = [l.strip() for l in f.readlines() if l.strip()]
            
            final_lines.extend(label_lines)

            with open(label_path, "w") as f:
                f.write("\n".join(final_lines))
            
            processed_count += 1
            if processed_count % 10 == 0:
                print(f"Processed {processed_count}/{len(image_files)}...", end="\r", file=sys.stderr)

        print(f"\nProcessed {processed_count} images.", file=sys.stderr)

        # Save updated data.yaml
        print("Updating data.yaml...", file=sys.stderr)
        yaml_content["names"] = current_names
        yaml_content["nc"] = len(current_names)

        with open(yaml_path, "w") as f:
            yaml.dump(yaml_content, f, sort_keys=False)

        # Archive results
        print(f"Zipping output to {output_zip}...", file=sys.stderr)
        
        # shutil.make_archive adds extension automatically, so we handle it
        output_base = str(output_zip.with_suffix(""))
        final_path = shutil.make_archive(output_base, 'zip', dataset_dir)

        print(f"Done. Saved to {final_path}", file=sys.stderr)
        print(final_path)
