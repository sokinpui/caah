import concurrent.futures
import io
import os
from pathlib import Path
from typing import Annotated, Any, Dict, List, Optional, Set, Tuple

import typer
from cvat_sdk import make_client
from cvat_sdk.api_client import models
from dotenv import load_dotenv
from PIL import Image

from yolo_model import YoloModel


def annotate(
    model_path: Annotated[
        Path, typer.Option("--model", "-m", help="Path to YOLO model file (.pt).")
    ],
    task_id: Annotated[int, typer.Option("--task-id", help="CVAT Task ID.")],
    device: Annotated[str, typer.Option(help="Device (cpu, gpu).")] = "cpu",
    conf: Annotated[float, typer.Option(help="Confidence threshold.")] = 0.25,
    ioa: Annotated[
        float, typer.Option(help="IoA threshold to drop old annotations.")
    ] = 0.5,
    jobs: Annotated[
        int, typer.Option("--jobs", "-j", help="Number of parallel jobs.")
    ] = 4,
    batch_size: Annotated[
        int, typer.Option("--batch", "-b", help="Inference batch size.")
    ] = 16,
) -> None:
    """Main execution flow for auto-annotation."""
    load_dotenv()
    model = _load_yolo_model(str(model_path), device)

    url, user, password = (
        os.getenv("CVAT_URL"),
        os.getenv("CVAT_USERNAME"),
        os.getenv("CVAT_PASSWORD"),
    )
    nas_path_str = os.getenv("NAS_PATH")
    nas_path = Path(nas_path_str) if nas_path_str else None

    if not all([url, user, password]):
        raise ValueError("CVAT credentials not found in environment variables.")

    print(f"Connecting to CVAT at {url}...")

    with make_client(url, credentials=(user, password)) as client:
        print(f"Fetching task {task_id}...")
        task = client.tasks.retrieve(task_id)

        # Fetch metadata to get original filenames for NAS optimization
        meta = task.get_meta()
        frame_filenames = {i: frame.name for i, frame in enumerate(meta.frames)}

        all_annotations = task.get_annotations()

        labels = task.get_labels()
        label_map = {l.name: l.id for l in labels}
        source_attr_map = {
            label.id: attr.id
            for label in labels
            for attr in label.attributes
            if attr.name == "source"
        }

        existing_by_frame = {}
        for s in all_annotations.shapes:
            if s.type.value == "rectangle":
                existing_by_frame.setdefault(s.frame, []).append(s)

        print(f"Task has {task.size} frames. Starting inference...")
        if nas_path:
            print(f"NAS optimization enabled. Checking: {nas_path}")

        new_shapes: List[models.LabeledShapeRequest] = []
        dropped_ids: Set[int] = set()

        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
            for batch_start in range(0, task.size, batch_size):
                batch_end = min(batch_start + batch_size, task.size)
                frame_ids = list(range(batch_start, batch_end))

                # Parallel Fetch
                images = list(
                    executor.map(
                        lambda fid: _get_frame_image(
                            fid, task, frame_filenames.get(fid), nas_path
                        ),
                        frame_ids,
                    )
                )

                # Batch Inference
                batch_results = model.predict(images)

                # Post-process
                for fid, frame_preds in zip(frame_ids, batch_results):
                    f_shapes, f_dropped = _process_predictions(
                        frame_id=fid,
                        predictions=frame_preds,
                        label_map=label_map,
                        source_attr_map=source_attr_map,
                        frame_existing=existing_by_frame.get(fid, []),
                        ioa_threshold=ioa,
                    )
                    new_shapes.extend(f_shapes)
                    dropped_ids.update(f_dropped)

                print(f"Processed frame {batch_end}/{task.size}...", end="\r")

        def _clean_for_request(annotation_list, dropped_set, request_type):
            cleaned = []
            for item in annotation_list:
                if item.id in dropped_set:
                    continue
                item_dict = item.to_dict()
                item_dict.pop("id", None)
                cleaned.append(request_type(**item_dict))
            return cleaned

        kept_shapes = _clean_for_request(
            all_annotations.shapes, dropped_ids, models.LabeledShapeRequest
        )
        kept_tracks = _clean_for_request(
            all_annotations.tracks, dropped_ids, models.LabeledTrackRequest
        )
        kept_tags = _clean_for_request(
            all_annotations.tags, dropped_ids, models.LabeledImageRequest
        )

        task.set_annotations(
            models.LabeledDataRequest(
                shapes=kept_shapes + new_shapes,
                tracks=kept_tracks,
                tags=kept_tags,
            )
        )

    print(f"\nDone. Annotated task {task_id}.")


def _process_predictions(
    frame_id: int,
    predictions: List[Dict],
    label_map: Dict[str, int],
    source_attr_map: Dict[int, int],
    frame_existing: List[Any],
    ioa_threshold: float,
) -> Tuple[List[models.LabeledShapeRequest], Set[int]]:
    """Processes model output into CVAT requests."""
    new_shapes = []
    dropped_ids = set()

    for pred in predictions:
        class_name = pred["label"]
        if class_name not in label_map:
            continue

        for exist in frame_existing:
            if _calculate_ioa(pred["box"], exist.points) <= ioa_threshold:
                continue

            exist_source = (
                exist.source.value if hasattr(exist.source, "value") else exist.source
            )
            if exist_source != "manual":
                dropped_ids.add(exist.id)

        l_id = label_map[class_name]
        attributes = []
        if l_id in source_attr_map:
            attributes.append(
                models.AttributeValRequest(spec_id=source_attr_map[l_id], value="auto")
            )

        new_shapes.append(
            models.LabeledShapeRequest(
                type=models.ShapeType("rectangle"),
                frame=frame_id,
                label_id=l_id,
                points=pred["box"],
                rotation=0,
                attributes=attributes,
                source="auto",
            )
        )

    return new_shapes, dropped_ids


def _get_frame_image(
    frame_id: int, task: Any, filename: Optional[str], nas_path: Optional[Path]
) -> Optional[Image.Image]:
    """Retrieves image from NAS or CVAT API."""
    if nas_path and filename:
        local_file = nas_path / filename
        if local_file.exists():
            try:
                return Image.open(local_file)
            except Exception:
                pass

    try:
        return Image.open(io.BytesIO(task.get_frame(frame_id).read()))
    except Exception:
        return None


def _calculate_ioa(new_box: list[float], old_box: list[float]) -> float:
    """Calculate Intersection over Area (IoA) relative to the old box."""
    x_min, y_min = max(new_box[0], old_box[0]), max(new_box[1], old_box[1])
    x_max, y_max = min(new_box[2], old_box[2]), min(new_box[3], old_box[3])

    if x_max <= x_min or y_max <= y_min:
        return 0.0

    intersection_area = (x_max - x_min) * (y_max - y_min)
    old_area = (old_box[2] - old_box[0]) * (old_box[3] - old_box[1])

    return intersection_area / old_area if old_area > 0 else 0.0


def _load_yolo_model(model_path_str: str, device: str) -> YoloModel:
    """Loads a YOLO model, handling errors."""
    model_path = Path(model_path_str)
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")

    try:
        return YoloModel(str(model_path), device=device)
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")
