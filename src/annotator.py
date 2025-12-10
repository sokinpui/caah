import argparse
import sys
import shutil
import tempfile
import zipfile
import yaml
from pathlib import Path

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


def run_annotate(args):
    """
    Main execution flow for auto-annotation.
    """
    model_path = Path(args.model)
    input_zip = Path(args.dataset)
    output_zip = Path(args.output)

    if not model_path.exists():
        print(f"Error: Model file not found at {model_path}", file=sys.stderr)
        sys.exit(1)

    if not input_zip.exists():
        print(f"Error: Input dataset not found at {input_zip}", file=sys.stderr)
        sys.exit(1)

    # Initialize model
    try:
        model = YoloModel(str(model_path), device=args.device)
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
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

        count = 0
        for img_path in image_files:
            # Get image dimensions
            img_w, img_h = model.get_image_size(img_path)
            
            # Predict
            predictions = model.predict(img_path)
            
            # Prepare label content
            label_lines = []
            for pred in predictions:
                class_id = pred["class_id"]
                box = pred["box"]
                
                xc, yc, w, h = _xyxy_to_yolo(box, img_w, img_h)
                label_lines.append(f"{class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}")

            # Write label file (same name as image, but .txt)
            label_path = img_path.with_suffix(".txt")
            with open(label_path, "w") as f:
                f.write("\n".join(label_lines))
            
            count += 1
            if count % 10 == 0:
                print(f"Processed {count}/{len(image_files)} images...", end="\r", file=sys.stderr)

        print(f"\nAnnotated {count} images.", file=sys.stderr)

        # Update or Create data.yaml to match the model's classes
        # This is crucial because the class_ids in .txt files correspond to this model
        print("Updating data.yaml with model classes...", file=sys.stderr)
        
        # Try to find existing data.yaml to preserve paths
        existing_yaml = list(dataset_dir.rglob("data.yaml"))
        yaml_content = {
            "train": "images/train", # Default fallback
            "val": "images/val",     # Default fallback
        }

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

        # Overwrite names with model names to ensure consistency
        yaml_content["names"] = model.model.names
        # Ensure nc (number of classes) matches
        yaml_content["nc"] = len(model.model.names)

        with open(yaml_path, "w") as f:
            yaml.dump(yaml_content, f, sort_keys=False)

        # Archive results
        print(f"Zipping output to {output_zip}...", file=sys.stderr)
        
        # shutil.make_archive adds extension automatically, so we handle it
        output_base = str(output_zip.with_suffix(""))
        final_path = shutil.make_archive(output_base, 'zip', dataset_dir)

        print(f"Done. Saved to {final_path}", file=sys.stderr)
        print(final_path)
