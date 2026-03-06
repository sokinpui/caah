import logging
import shutil
import sys
import zipfile
from pathlib import Path
from typing import List, Optional

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def setup_logging(log_file: str = "caah.log", level: int = logging.INFO):
    logger = logging.getLogger()
    if logger.handlers:
        return

    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def resolve_device(device: str) -> str:
    """Resolves the device string to a valid torch/ultralytics device."""
    import torch

    if device == "cpu":
        return "cpu"

    if device != "gpu":
        return device

    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"

    print(
        "Warning: GPU requested but not available. Falling back to CPU.",
        file=sys.stderr,
    )
    return "cpu"


def extract_zip(zip_path: Path, dest_path: Path) -> None:
    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file not found: {zip_path}")
    dest_path.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(dest_path)


def create_zip(source_path: Path, output_zip: Path) -> None:
    if output_zip.exists():
        output_zip.unlink()
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for file in source_path.rglob("*"):
            if file.is_file():
                z.write(file, file.relative_to(source_path))


def calculate_ioa(box1: List[float], box2: List[float]) -> float:
    """Calculate Intersection over Area (IoA) relative to the second box."""
    x_min, y_min = max(box1[0], box2[0]), max(box1[1], box2[1])
    x_max, y_max = min(box1[2], box2[2]), min(box1[3], box2[3])

    if x_max <= x_min or y_max <= y_min:
        return 0.0

    intersection_area = (x_max - x_min) * (y_max - y_min)
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

    return intersection_area / area2 if area2 > 0 else 0.0


def strip_prefix(path_str: str, prefix: str) -> str:
    if not prefix or not path_str.startswith(prefix):
        return path_str
    return path_str[len(prefix) :].lstrip("/")


def find_file(
    directory: Path, patterns: List[str], recursive: bool = True
) -> Optional[Path]:
    """Finds the first file matching any of the provided patterns."""
    for pattern in patterns:
        matches = list(
            directory.rglob(pattern) if recursive else directory.glob(pattern)
        )
        if matches:
            return matches[0]
    return None
