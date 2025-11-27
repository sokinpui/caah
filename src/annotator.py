from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path


class UnsupportedFormatException(Exception):
    pass


class Model:
    """
    A placeholder for a real model inference engine.
    In a real implementation, this class would load a trained model
    and use it to predict annotations for an image.
    """

    def __init__(self, model_path: str):
        model_file = Path(model_path)
        if not model_file.exists():
            raise FileNotFoundError(f"Model path does not exist: {model_path}")
        self.model_path = model_path
        # In a real implementation, you would load the model here, e.g.,
        # self.model = torch.load(model_path)
        print(f"Model loaded from {model_path}")

    def predict(self, image_path: str) -> list[dict]:
        """
        This is a placeholder for the actual model prediction.
        It should return annotations in a structured format.
        """
        print(f"Predicting for image: {image_path}")
        # Example output: a list of detections
        # Each detection is a dictionary with label and bounding box [xmin, ymin, xmax, ymax]
        return [
            {"label": "car", "box": [100, 150, 250, 300]},
            {"label": "person", "box": [280, 80, 350, 320]},
        ]


class AnnotationFormatter(ABC):
    """
    Abstract base class for annotation formatters.
    """

    def __init__(self):
        self.output_dir = None

    def initialize(self, output_dir: Path, image_paths: list[Path]):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

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

    def save_per_image(
        self, image_path: Path, annotations: list[dict], image_size: tuple[int, int]
    ):
        # In a real scenario, you would need a mapping from label names to class indices
        label_to_id = {"car": 0, "person": 1}  # Example mapping
        image_width, image_height = image_size

        lines = []
        for ann in annotations:
            label = ann.get("label")
            if label not in label_to_id:
                continue

            class_id = label_to_id[label]
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
        print(f"Saved YOLO annotations to {output_path}")


class CvatXmlFormatter(AnnotationFormatter):
    """
    Formats annotations in CVAT XML format.
    Saves a single annotations.xml file.
    """

    def initialize(self, output_dir: Path, image_paths: list[Path]):
        super().initialize(output_dir, image_paths)
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

        # This should be more dynamic, but for now it's ok.
        labels_xml = """        <label><name>car</name><color>#ff0000</color><attributes></attributes></label>
        <label><name>person</name><color>#00ff00</color><attributes></attributes></label>"""

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
        print(f"Saved CVAT annotations to {output_path}")


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

    def __init__(self, model_path: str):
        self.model = Model(model_path)

    def get_image_size(self, image_path: Path) -> tuple[int, int]:
        """
        Placeholder for getting image size.
        A library like Pillow would be needed for a real implementation.
        """
        # from PIL import Image
        # try:
        #     with Image.open(image_path) as img:
        #         return img.size
        # except IOError:
        #     print(f"Warning: Could not read image size for {image_path}. Using default.")
        #     return (1920, 1080)
        return (1920, 1080)  # Dummy size

    def process_images(
        self, images_dir: Path, output_dir: Path, formatter: AnnotationFormatter
    ):
        image_extensions = [".jpg", ".jpeg", ".png"]
        image_paths = sorted(
            [p for p in images_dir.iterdir() if p.suffix.lower() in image_extensions]
        )

        if not image_paths:
            print(f"No images found in {images_dir}")
            return

        formatter.initialize(output_dir, image_paths)

        for image_path in image_paths:
            annotations = self.model.predict(str(image_path))
            image_size = self.get_image_size(image_path)
            formatter.save_per_image(image_path, annotations, image_size)

        formatter.finalize()
