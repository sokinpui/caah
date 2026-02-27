import threading
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union, Optional

from utils import resolve_device


class YoloModel:
    """
    A class for loading a YOLO model and performing inference.
    """

    def __init__(self, model_path: str, device: str = "gpu"):
        from ultralytics import YOLO

        model_file = Path(model_path)
        if not model_file.exists():
            raise FileNotFoundError(f"Model path does not exist: {model_path}")

        self.model = YOLO(model_path)
        self.device = resolve_device(device)
        self.labels = self.model.names
        self._lock = threading.Lock()
        print(f"YOLO model loaded from {model_path}", file=sys.stderr)
        print(f"Using device: {self.device}", file=sys.stderr)

    def predict(self, image_source: Union[Path, Any, List[Any]]) -> Union[List[Dict], List[List[Dict]]]:
        """
        Performs inference on image(s) and returns annotations.
        Supports batch processing if a list is provided.
        """
        is_batch = isinstance(image_source, list)
        sources = image_source if is_batch else [image_source]

        # Filter out None values which might come from failed image fetches
        valid_sources = [s for s in sources if s is not None]
        if not valid_sources:
            return [[]] * len(sources) if is_batch else []

        with self._lock:
            results = self.model(valid_sources, verbose=False, device=self.device)

        # Map results back to the original input indices (handling Nones)
        all_annotations = []
        result_idx = 0
        
        for src in sources:
            if src is None:
                all_annotations.append([])
                continue
            
            res = results[result_idx]
            result_idx += 1
            
            frame_preds = []
            boxes = res.boxes
            names = res.names

            for box in boxes:
                xyxy = box.xyxy[0].cpu().numpy().tolist()
                class_id = int(box.cls[0].cpu().numpy())
                label = names[class_id]
                box_coords = [int(coord) for coord in xyxy]

                frame_preds.append({
                    "label": label,
                    "class_id": class_id,
                    "box": box_coords,
                })
            all_annotations.append(frame_preds)

        return all_annotations if is_batch else all_annotations[0]

    def get_image_size(self, image_path: Path) -> Tuple[int, int]:
        """
        Gets the width and height of an image.
        """
        import cv2

        img = cv2.imread(str(image_path))
        if img is None:
            print(
                f"Warning: Could not read image size for {image_path}. Using default.",
                file=sys.stderr,
            )
            return (1920, 1080)
        height, width, _ = img.shape
        return (width, height)
