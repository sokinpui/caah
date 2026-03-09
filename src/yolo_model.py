import sys
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from utils import resolve_device


class YoloModel:
    """
    A class for loading a YOLO model and performing inference.
    """

    def __init__(self, model_path: str, device: str = "gpu"):
        from ultralytics import YOLO

        model_file = Path(model_path)
        self.model_path = model_path
        if not model_file.exists():
            raise FileNotFoundError(f"Model path does not exist: {model_path}")

        self.model = YOLO(model_path)
        self.device = resolve_device(device)
        self.labels = self.model.names
        self._lock = threading.Lock()
        self._sahi_model = None
        print(f"YOLO model loaded from {model_path}", file=sys.stderr)
        print(f"Using device: {self.device}", file=sys.stderr)

    def predict(
        self,
        image_source: Union[Path, Any, List[Any]],
        sahi: bool = False,
        slice_h: int = 640,
        slice_w: int = 640,
        overlap_h: float = 0.2,
        overlap_w: float = 0.2,
    ) -> Union[List[Dict], List[List[Dict]]]:
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

        if sahi:
            results = [
                self._predict_sahi(
                    src,
                    slice_h=slice_h,
                    slice_w=slice_w,
                    overlap_h=overlap_h,
                    overlap_w=overlap_w,
                )
                for src in valid_sources
            ]
            return self._format_results(sources, results) if is_batch else results[0]

        with self._lock:
            results = self.model(valid_sources, verbose=False, device=self.device)

        # Map results back to the original input indices (handling Nones)
        all_annotations = []
        result_idx = 0

        return (
            self._format_results(sources, results)
            if is_batch
            else self._format_results(sources, results)[0]
        )

    def _format_results(
        self, sources: List[Any], results: List[Any]
    ) -> List[List[Dict]]:
        """Standardizes output from both native YOLO and SAHI results."""
        all_annotations = []
        result_idx = 0

        for src in sources:
            if src is None:
                all_annotations.append([])
                continue

            res = results[result_idx]
            result_idx += 1

            frame_preds = []

            # Handle SAHI PredictionResult
            if hasattr(res, "object_prediction_list"):
                for pred in res.object_prediction_list:
                    bbox = pred.bbox.to_xyxy()
                    frame_preds.append(
                        {
                            "label": pred.category.name,
                            "class_id": pred.category.id,
                            "box": [int(c) for c in bbox],
                        }
                    )
            # Handle Ultralytics Result
            else:
                boxes = res.boxes
                names = res.names
                for box in boxes:
                    xyxy = box.xyxy[0].cpu().numpy().tolist()
                    class_id = int(box.cls[0].cpu().numpy())
                    frame_preds.append(
                        {
                            "label": names[class_id],
                            "class_id": class_id,
                            "box": [int(coord) for coord in xyxy],
                        }
                    )

            all_annotations.append(frame_preds)
        return all_annotations

    def _predict_sahi(self, image: Any, **kwargs) -> Any:
        """Internal helper for SAHI sliced inference."""
        import numpy as np
        from sahi.predict import get_sliced_prediction

        if self._sahi_model is None:
            from sahi import AutoDetectionModel

            self._sahi_model = AutoDetectionModel.from_pretrained(
                model_type="ultralytics",
                model_path=self.model_path,
                device=self.device,
                confidence_threshold=0.25,
            )

        # Convert PIL Image to numpy array if needed
        if hasattr(image, "mode") and hasattr(image, "convert"):
            # Assume PIL Image
            image = np.array(image.convert("RGB"))

        return get_sliced_prediction(
            image,
            self._sahi_model,
            slice_height=kwargs.get("slice_h", 640),
            slice_width=kwargs.get("slice_w", 640),
            overlap_height_ratio=kwargs.get("overlap_h", 0.2),
            overlap_width_ratio=kwargs.get("overlap_w", 0.2),
            verbose=0,
        )

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
