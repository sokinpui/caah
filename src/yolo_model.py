from pathlib import Path

import cv2
from ultralytics import YOLO


class YoloModel:
    """
    A class for loading a YOLO model and performing inference.
    """

    def __init__(self, model_path: str):
        model_file = Path(model_path)
        if not model_file.exists():
            raise FileNotFoundError(f"Model path does not exist: {model_path}")

        self.model = YOLO(model_path)
        self.labels = self.model.names
        print(f"YOLO model loaded from {model_path}")

    def predict(self, image_path: Path) -> list[dict]:
        """
        Performs inference on a single image and returns annotations.
        """
        print(f"Predicting for image: {image_path}")

        # The ultralytics library can take a Path object directly
        results = self.model(image_path, verbose=False)

        annotations = []

        # Results is a list, but for a single image it has one element
        if not results:
            return []

        result = results[0]
        boxes = result.boxes
        names = result.names

        for box in boxes:
            # Bounding box in xyxy format
            xyxy = box.xyxy[0].cpu().numpy().tolist()
            # Class index
            class_id = int(box.cls[0].cpu().numpy())

            # Get label name from class index
            label = names[class_id]

            # Convert box coordinates to integers
            box_coords = [int(coord) for coord in xyxy]

            annotations.append(
                {
                    "label": label,
                    "box": box_coords,
                }
            )

        return annotations

    def get_image_size(self, image_path: Path) -> tuple[int, int]:
        """
        Gets the width and height of an image.
        """
        img = cv2.imread(str(image_path))
        if img is None:
            print(
                f"Warning: Could not read image size for {image_path}. Using default."
            )
            return (1920, 1080)
        height, width, _ = img.shape
        return (width, height)
