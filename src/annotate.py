import concurrent.futures
import io
import os
from pathlib import Path
from typing import Annotated, Any, Dict, List, Optional, Set, Tuple

import typer

from utils import calculate_ioa, strip_prefix


def annotate(
    model_path: Annotated[
        Path, typer.Option("--model", "-m", help="Path to YOLO model file (.pt).")
    ],
    task_id: Annotated[
        Optional[int], typer.Option("--id", "-i", help="CVAT Task ID.")
    ] = None,
    task_ids: Annotated[Optional[str], typer.Option("--ids", help="Task IDs.")] = None,
    device: Annotated[
        str, typer.Option("--device", "-d", help="Device (cpu, gpu).")
    ] = "gpu",
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
    sahi: Annotated[
        bool, typer.Option("--sahi", help="Enable Sliced Inference.")
    ] = False,
    size: Annotated[
        str, typer.Option("--size", help="SAHI slice size as H:W.")
    ] = "640:640",
    overlap: Annotated[
        str, typer.Option("--overlap", help="SAHI overlap ratio as H:W.")
    ] = "0.2:0.2",
) -> None:
    """Main execution flow for auto-annotation."""
    from cvat_sdk import make_client
    from dotenv import load_dotenv

    load_dotenv()

    target_ids = []
    if task_id:
        target_ids.append(task_id)
    if task_ids:
        target_ids.extend([int(tid) for tid in task_ids.split()])

    if not target_ids:
        raise ValueError("No Task ID provided. Use --id or --ids.")

    model = _load_yolo_model(str(model_path), device)

    sh, sw = map(int, size.split(":"))
    oh, ow = map(float, overlap.split(":"))

    url, user, password = (
        os.getenv("CVAT_URL"),
        os.getenv("CVAT_USERNAME"),
        os.getenv("CVAT_PASSWORD"),
    )
    nas_path_str = os.getenv("NAS_PATH")
    nas_prefix = os.getenv("NAS_PREFIX", "")
    nas_path = Path(nas_path_str) if nas_path_str else None

    if not all([url, user, password]):
        raise ValueError("CVAT credentials not found in environment variables.")

    print(f"Connecting to CVAT at {url}...")

    with make_client(url, credentials=(user, password)) as client:
        for tid in target_ids:
            _annotate_task(
                client=client,
                task_id=tid,
                model=model,
                batch_size=batch_size,
                jobs=jobs,
                ioa=ioa,
                sahi=sahi,
                size=(sh, sw),
                overlap=(oh, ow),
                nas_path=nas_path,
                nas_prefix=nas_prefix,
            )

    print(f"\nDone. Processed {len(target_ids)} tasks.")


def _annotate_task(
    client: Any,
    task_id: int,
    model: Any,
    batch_size: int,
    jobs: int,
    ioa: float,
    sahi: bool,
    size: Tuple[int, int],
    overlap: Tuple[float, float],
    nas_path: Optional[Path],
    nas_prefix: str,
) -> None:
    """Internal logic to process a single task."""
    from cvat_sdk.api_client import models

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

    print(f"Task {task_id} has {task.size} frames. Starting inference...")
    if nas_path:
        print(f"NAS optimization enabled for task {task_id}.")

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
                        fid, task, frame_filenames.get(fid), nas_path, nas_prefix
                    ),
                    frame_ids,
                )
            )

            # Batch Inference
            batch_results = model.predict(
                images,
                sahi=sahi,
                slice_h=size[0],
                slice_w=size[1],
                overlap_h=overlap[0],
                overlap_w=overlap[1],
            )

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

    print(f"\nAnnotated task {task_id}.")


def _process_predictions(
    frame_id: int,
    predictions: List[Dict],
    label_map: Dict[str, int],
    source_attr_map: Dict[int, int],
    frame_existing: List[Any],
    ioa_threshold: float,
) -> Tuple[List[Any], Set[int]]:
    """Processes model output into CVAT requests."""
    from cvat_sdk.api_client import models

    new_shapes = []
    dropped_ids = set()

    for pred in predictions:
        class_name = pred["label"]
        if class_name not in label_map:
            continue

        for exist in frame_existing:
            if calculate_ioa(pred["box"], exist.points) <= ioa_threshold:
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
    frame_id: int,
    task: Any,
    filename: Optional[str],
    nas_path: Optional[Path],
    prefix: str = "",
) -> Optional[Any]:
    """Retrieves image from NAS or CVAT API."""
    from PIL import Image

    if nas_path and filename:
        clean_name = strip_prefix(filename, prefix)

        local_file = nas_path / clean_name

        if local_file.exists():
            try:
                return Image.open(local_file)
            except Exception:
                pass

    try:
        return Image.open(io.BytesIO(task.get_frame(frame_id).read()))
    except Exception:
        return None


def _load_yolo_model(model_path_str: str, device: str) -> Any:
    """Loads a YOLO model, handling errors."""
    from yolo_model import YoloModel

    model_path = Path(model_path_str)
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")

    try:
        return YoloModel(str(model_path), device=device)
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")
