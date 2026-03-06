import os
import shutil
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv, set_key
from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from annotate import annotate as run_annotate
from cvat import _get_api
from utils import setup_logging
from train import process_dataset_and_train

setup_logging()

app = FastAPI(title="CAAH API", description="Cvat Auto Annotation Helper API")

UPLOAD_DIR = Path("output/uploads")
EXPORT_DIR = Path("output/exports")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

# --- Models ---


class ConfigUpdate(BaseModel):
    value: str


class ExportRequest(BaseModel):
    id: int
    format: str = "YOLO 1.1"
    only_manual: bool = False


class TrainRequest(BaseModel):
    data_path: str
    model: str = "yolo11n"
    epochs: int = 50
    batch: int = 16
    device: str = "gpu"
    split: Optional[str] = None


class AnnotateRequest(BaseModel):
    task_id: int
    model_path: str
    device: str = "cpu"
    conf: float = 0.25
    ioa: float = 0.5
    jobs: int = 4


# --- Helper Functions ---


def update_env(key: str, value: str):
    env_path = Path(".env")
    if not env_path.exists():
        env_path.touch()
    set_key(str(env_path), key, value)
    load_dotenv(override=True)


async def save_upload(file: UploadFile) -> Path:
    dest = UPLOAD_DIR / file.filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return dest


# --- Endpoints ---


# Update Env
@app.post("/config/cvatHost")
def set_cvat_host(cfg: ConfigUpdate):
    update_env("CVAT_URL", cfg.value)
    return {"status": "ok"}


@app.post("/config/cvatUsername")
def set_cvat_username(cfg: ConfigUpdate):
    update_env("CVAT_USERNAME", cfg.value)
    return {"status": "ok"}


@app.post("/config/cvatPassword")
def set_cvat_password(cfg: ConfigUpdate):
    update_env("CVAT_PASSWORD", cfg.value)
    return {"status": "ok"}


@app.post("/config/nasPath")
def set_nas_path(cfg: ConfigUpdate):
    update_env("NAS_PATH", cfg.value)
    return {"status": "ok"}


# CVAT Operations
@app.post("/task/export")
def export_task(req: ExportRequest, background_tasks: BackgroundTasks):
    api = _get_api()
    output_path = EXPORT_DIR / f"task_{req.id}_export.zip"
    background_tasks.add_task(
        api.export_task_dataset,
        req.id,
        str(output_path),
        req.format,
        True,
        req.only_manual,
    )
    return {"status": "started", "output": str(output_path)}


@app.post("/project/export")
def export_project(req: ExportRequest, background_tasks: BackgroundTasks):
    api = _get_api()
    output_path = EXPORT_DIR / f"project_{req.id}_export.zip"
    background_tasks.add_task(
        api.export_project_dataset,
        req.id,
        str(output_path),
        req.format,
        True,
        req.only_manual,
    )
    return {"status": "started", "output": str(output_path)}


# Train Operations
@app.post("/train/upload/weight")
async def upload_train_weight(file: UploadFile = File(...)):
    if not file.filename.endswith(".pt"):
        raise HTTPException(400, "Only .pt files allowed")
    path = await save_upload(file)
    return {"status": "uploaded", "path": str(path)}


@app.post("/train/start")
def start_train(req: TrainRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        process_dataset_and_train,
        req.data_path,
        req.model,
        req.epochs,
        640,
        req.batch,
        req.device,
        req.split,
    )
    return {"status": "training started"}


@app.get("/train/config")
def get_train_config():
    return {"default_epochs": 50, "default_batch": 16, "imgsz": 640}


# Annotate Operations
@app.post("/annotate/start")
def start_annotate(req: AnnotateRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        run_annotate,
        Path(req.model_path),
        req.task_id,
        req.device,
        req.conf,
        req.ioa,
        req.jobs,
    )
    return {"status": "annotation started"}


@app.post("/annotate/upload/weight")
async def upload_annotate_weight(file: UploadFile = File(...)):
    return await upload_train_weight(file)
