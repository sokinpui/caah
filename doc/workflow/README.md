# Standard Workflow Guide

This document defines the standard operating procedure for preparing datasets, training models, and performing auto-annotation. The workflow is designed to handle high-resolution imagery through tiling (slicing) to improve detection performance on small objects.

## 1. Infrastructure Requirements

The machine running `caah` must have:

- **Network Access**: Connectivity to the CVAT server API.
- **NAS Access**: The same Network Attached Storage (NAS) used by CVAT must be mounted locally.
- **Environment**: A `.env` file configured with `CVAT_URL`, `CVAT_USERNAME`, `CVAT_PASSWORD`, and `NAS_PATH`.

## 1.1 Environment Configuration (.env)

The following variables are required for the full feature set:

| Variable            | Description                                                                         |
| :------------------ | :---------------------------------------------------------------------------------- |
| `CVAT_URL`          | The endpoint of your primary CVAT server.                                           |
| `CVAT_USERNAME`     | Admin/User for primary CVAT.                                                        |
| `CVAT_PASSWORD`     | Password for primary CVAT.                                                          |
| `NAS_PATH`          | The local mount point where your images are stored (e.g., `/mnt/network`).          |
| `NAS_PREFIX`        | Internal CVAT folder prefix (e.g., `RNT`). `caah` strips this to match local files. |
| `CVAT_URL_2`        | The endpoint of the source/old CVAT server (for migrations).                        |
| `CVAT_USERNAME_2`   | Admin/User for source CVAT.                                                         |
| `CVAT_PASSWORD_2`   | Password for source CVAT.                                                           |
| `CVAT_SHARE_PATH`   | The absolute path inside the target CVAT container for shared storage.              |
| `CVAT_SHARE_PATH_2` | The absolute path inside the source CVAT container for shared storage.              |

**Example `.env` snippet:**

```ini
NAS_PATH=/mnt/network
NAS_PREFIX=RNT
CVAT_SHARE_PATH=/home/django/share/RNT
CVAT_SHARE_PATH_2=/home/django/share
```

## 2. CVAT Project Setup

When creating tasks or projects in the CVAT WebUI:

1. **Storage Type**: Always use **"Connected File Share"**.
2. **Path**: Select the images from the NAS mount point.
3. **Benefit**: This allows CVAT to reference images directly without uploading them to its internal database.

## 3. The Tiling Workflow

To achieve the best results with high-resolution images, follow these steps to slice the dataset before training.

### 3.1 Export Dataset

Export the project or task from CVAT in **YOLO 1.1** format. Ensure images are included.

```bash
caah cvat project export_dataset \
  --project-id 1 \
  --images \
  --output-file raw_dataset.zip
```

### 3.2 Format Conversion (YOLO to COCO)

The slicing utility requires COCO format.

```bash
caah dataset yolo2coco raw_dataset.zip raw_coco.zip
```

### 3.3 Dataset Slicing

Tile the images into smaller patches (e.g., 640x640). This is critical for detecting small objects in large frames.

```bash
caah dataset slice raw_coco.zip sliced_coco.zip --size 640:640 --overlap 0.2:0.2
```

### 3.4 Format Conversion (COCO to YOLO)

Convert the sliced patches back to YOLO format for training.

```bash
caah dataset coco2yolo sliced_coco.zip sliced_yolo.zip
```

## 4. Training

Train the model using the sliced dataset. Since the patches are extracted locally, do not use the `--network-drive` flag for this specific dataset.

```bash
caah train \
  -m yolo11s \
  --data sliced_yolo.zip \
  --split 8:2 \
  --epochs 1000 \
  --batch 32 \
  --imgsz 640 \
  --device 0 \
  --workers 0 \
  --save-period 10 \
  -a my_aug.py \
  --project "MTR-Bird-Model" \
  --name "yolo11s-640-20260306-custom"
```

## 5. Auto-Annotation

**Note**: Auto-annotation is performed on the original full-sized images in CVAT. The model trained on slices will run inference on the full frames.

Once you have a trained model, apply it to new tasks. `caah` will attempt to read images directly from the NAS if `NAS_PATH` is configured, falling back to the CVAT API only if necessary.

```bash
caah annotate \
  --model ./runs/MTR-Bird-Model/yolo11s-640-20260306-custom/weights/best.pt \
  --task-id 123 \
  --device gpu \
  --conf 0.3 \
  --ioa 0.5

### Key Advantages of this Workflow
- **Zero Image Duplication**: Images stay on the NAS.
- **Small Object Detection**: Slicing high-resolution images prevents features from being lost during resizing.
- **CVAT Integration**: Inference results are mapped back to the original frames automatically.
- **Consistency**: The same image paths are used across CVAT, training, and inference.
```
