import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml

from yolo_model import YoloModel


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


def run_offline(args, model):
    """
    Main execution flow for offline auto-annotation.
    """
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
