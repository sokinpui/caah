import sys

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


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
