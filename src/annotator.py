import argparse
import shutil
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from yolo_model import YoloModel


class UnsupportedFormatException(Exception):
    pass


class AnnotationFormatter(ABC):
    """
    Abstract base class for annotation formatters.
    """

    def __init__(self):
        self.output_dir = None

    def initialize(
        self, output_dir: Path, image_paths: list[Path], labels: dict = None
    ):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.labels = labels if labels else {}

    @abstractmethod
    def save_per_image(
        self, image_path: Path, annotations: list[dict], image_size: tuple[int, int]
    ):
        pass

    def finalize(self):
        pass


class YoloFormatter(AnnotationFormatter):
    """
    Formats annotations in YOLO format.
    Saves one .txt file per image.
    """

    def initialize(
        self, output_dir: Path, image_paths: list[Path], labels: dict = None
    ):
        super().initialize(output_dir, image_paths, labels)
        self.label_to_id = {name: i for i, name in self.labels.items()}

    def save_per_image(
        self, image_path: Path, annotations: list[dict], image_size: tuple[int, int]
    ):
        # In a real scenario, you would need a mapping from label names to class indices
        image_width, image_height = image_size

        lines = []
        for ann in annotations:
            label = ann.get("label")
            if label not in self.label_to_id:
                continue

            class_id = self.label_to_id[label]
            x_min, y_min, x_max, y_max = ann.get("box", [0, 0, 0, 0])

            x_center = (x_min + x_max) / 2 / image_width
            y_center = (y_min + y_max) / 2 / image_height
            box_width = (x_max - x_min) / image_width
            box_height = (y_max - y_min) / image_height

            lines.append(
                f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"
            )

        output_filename = image_path.with_suffix(".txt").name
        output_path = self.output_dir / output_filename
        output_path.write_text("\n".join(lines))
        print(f"Saved YOLO annotations to {output_path}", file=sys.stderr)


class CvatXmlFormatter(AnnotationFormatter):
    """
    Formats annotations in CVAT XML format.
    Saves a single annotations.xml file.
    """

    def initialize(
        self, output_dir: Path, image_paths: list[Path], labels: dict = None
    ):
        super().initialize(output_dir, image_paths, labels)
        self.image_annotations = []
        self.image_paths = image_paths

    def save_per_image(
        self, image_path: Path, annotations: list[dict], image_size: tuple[int, int]
    ):
        image_id = self.image_paths.index(image_path)
        width, height = image_size

        box_strings = []
        for ann in annotations:
            label = ann.get("label")
            xtl, ytl, xbr, ybr = ann.get("box", [0, 0, 0, 0])
            box_strings.append(
                f'    <box label="{label}" occluded="0" source="auto" xtl="{xtl}" ytl="{ytl}" xbr="{xbr}" ybr="{ybr}" z_order="0"></box>'
            )

        boxes = "\n".join(box_strings)
        self.image_annotations.append(
            f"""  <image id="{image_id}" name="{image_path.name}" width="{width}" height="{height}">
{boxes}
  </image>"""
        )

    def finalize(self):
        all_annotations = "\n".join(self.image_annotations)
        num_images = len(self.image_paths)

        label_strings = []
        # A simple color generator
        colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff"]
        if self.labels:
            # self.labels is dict[int, str]
            for i, label_name in self.labels.items():
                color = colors[i % len(colors)]
                label_strings.append(
                    f"        <label><name>{label_name}</name><color>{color}</color><attributes></attributes></label>"
                )
        labels_xml = "\n".join(label_strings)

        now_iso = datetime.utcnow().isoformat()

        xml_output = f"""<?xml version="1.0" encoding="utf-8"?>
<annotations>
  <version>1.1</version>
  <meta>
    <task>
      <id></id>
      <name>Auto-annotated Task</name>
      <size>{num_images}</size>
      <mode>annotation</mode>
      <overlapping>0</overlapping>
      <bugtracker></bugtracker>
      <created>{now_iso}</created>
      <updated>{now_iso}</updated>
      <labels>
{labels_xml}
      </labels>
    </task>
    <dumped>{now_iso}</dumped>
  </meta>
{all_annotations}
</annotations>"""
        output_path = self.output_dir / "annotations.xml"
        output_path.write_text(xml_output)
        print(f"Saved CVAT annotations to {output_path}", file=sys.stderr)


def get_formatter(output_format: str) -> AnnotationFormatter:
    format_map = {
        "cvat": CvatXmlFormatter,
        "yolo": YoloFormatter,
    }
    formatter_class = format_map.get(output_format.lower())
    if not formatter_class:
        raise UnsupportedFormatException(f"Unsupported output format: {output_format}")
    return formatter_class()


class AutoAnnotator:
    """
    Orchestrates the auto-annotation process.
    """
    def __init__(self, model_path: str, device: str = "gpu"):
        self.model = YoloModel(model_path, device=device)

    def process_images(
        self,
        images_dir: Path,
        output_dir: Path,
        formatter: AnnotationFormatter,
        copy_images: bool = False,
    ):
        image_extensions = [".jpg", ".jpeg", ".png"]
        image_paths = sorted(
            [p for p in images_dir.iterdir() if p.suffix.lower() in image_extensions]
        )

        if not image_paths:
            print(f"No images found in {images_dir}", file=sys.stderr)
            return

        formatter.initialize(output_dir, image_paths, labels=self.model.labels)

        for image_path in image_paths:
            if copy_images:
                shutil.copy(image_path, output_dir)

            annotations = self.model.predict(image_path)
            image_size = self.model.get_image_size(image_path)
            formatter.save_per_image(image_path, annotations, image_size)

        formatter.finalize()


def add_annotate_arguments(parser):
    """
    Adds annotation-specific arguments to the parser.
    """
    parser.add_argument(
        "-m", "--model", type=str, required=True, help="Path to the trained model."
    )
    parser.add_argument(
        "-i",
        "--images",
        type=str,
        required=True,
        help="Path to the directory containing images.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Path to the directory to save annotations.",
    )
    parser.add_argument(
        "--output-format",
        type=str,
        default="cvat",
        choices=["cvat", "yolo"],
        help="Format for the output annotations.",
    )
    parser.add_argument(
        "-c",
        "--copy",
        action="store_true",
        help="Copy original images to the output directory.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="gpu",
        choices=["gpu", "cpu"],
        help="Device to run the model on (gpu or cpu).",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Suppress all messages except the final output path to stdout.",
    )


def run_annotate(args):
    """
    Runs the annotation process with parsed arguments.
    """
    images_path = Path(args.images)
    if not images_path.is_dir():
        print(f"Error: Image directory not found at {args.images}", file=sys.stderr)
        return

    try:
        annotator = AutoAnnotator(args.model, device=args.device)
        formatter = get_formatter(args.output_format)
        annotator.process_images(
            images_path, Path(args.output), formatter, copy_images=args.copy
        )
        print(args.output)
    except (FileNotFoundError, UnsupportedFormatException) as e:
        print(f"Error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)


def main():
    """
    Main function to run the auto-annotation process.
    It parses command-line arguments, initializes the annotator and formatter,
    and processes the images.
    """
    parser = argparse.ArgumentParser(
        description="Auto-annotate images using a trained model."
    )
    add_annotate_arguments(parser)
    args = parser.parse_args()
    run_annotate(args)


if __name__ == "__main__":
    main()
