import logging
import sys
from pathlib import Path

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

    return device
