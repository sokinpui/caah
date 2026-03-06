import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Optional

from datumaro.components.dataset import Dataset


def yolo_to_coco(input_zip: Path, output_zip: Path, nas_path: Optional[Path] = None, nas_prefix: str = ""):
    """
    Converts a YOLO format ZIP dataset to COCO instances format.
    Handles datasets with or without images automatically via Datumaro.
    """
    if not input_zip.is_file():
        raise FileNotFoundError(f"Input file not found: {input_zip}")

    with tempfile.TemporaryDirectory() as tmp_dir:
        working_dir = Path(tmp_dir)
        extract_path = working_dir / "extract"
        export_path = working_dir / "export"

        _extract_zip(input_zip, extract_path)

        if nas_path:
            _fill_images_from_nas(extract_path, nas_path, nas_prefix)

        dataset = Dataset.import_from(str(extract_path), format="yolo")
        dataset.export(str(export_path), format="coco_instances", save_media=True)

        _create_zip(export_path, output_zip)


def _fill_images_from_nas(extract_path: Path, nas_path: Path, nas_prefix: str):
    """Locates and copies missing images from NAS based on label filenames."""
    image_exts = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
    search_dir = extract_path / "obj_train_data"
    if not search_dir.exists():
        search_dir = extract_path

    label_files = list(search_dir.rglob("*.txt"))

    for lbl in label_files:
        if lbl.name in ["classes.txt", "obj.names"]:
            continue

        if any(lbl.with_suffix(ext).exists() for ext in image_exts):
            continue

        rel_p = str(lbl.relative_to(search_dir))
        if nas_prefix and rel_p.startswith(nas_prefix):
            rel_p = rel_p[len(nas_prefix) :].lstrip("/")

        for ext in image_exts:
            nas_img = nas_path / Path(rel_p).with_suffix(ext)
            if nas_img.exists():
                shutil.copy2(nas_img, lbl.with_suffix(ext))
                break


def _extract_zip(zip_path: Path, dest_path: Path):
    dest_path.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(dest_path)


def _create_zip(source_path: Path, output_zip: Path):
    if output_zip.exists():
        output_zip.unlink()

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for file in source_path.rglob("*"):
            if not file.is_file():
                continue
            z.write(file, file.relative_to(source_path))
