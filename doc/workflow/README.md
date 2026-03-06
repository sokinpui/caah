# Standard Workflow Guide

This document defines the preferred and most efficient way to use the `caah` toolchain. Following this workflow minimizes data transfer and avoids duplicating large image datasets.

## 1. Infrastructure Requirements

The machine running `caah` must have:
- **Network Access**: Connectivity to the CVAT server API.
- **NAS Access**: The same Network Attached Storage (NAS) used by CVAT must be mounted locally.
- **Environment**: A `.env` file configured with `CVAT_URL`, `CVAT_USERNAME`, `CVAT_PASSWORD`, and `NAS_PATH`.

## 1.1 Environment Configuration (.env)

The following variables are required for the full feature set:

| Variable | Description |
| :--- | :--- |
| `CVAT_URL` | The endpoint of your primary CVAT server. |
| `CVAT_USERNAME` | Admin/User for primary CVAT. |
| `CVAT_PASSWORD` | Password for primary CVAT. |
| `NAS_PATH` | The local mount point where your images are stored (e.g., `/mnt/network`). |
| `NAS_PREFIX` | Internal CVAT folder prefix (e.g., `RNT`). `caah` strips this to match local files. |
| `CVAT_URL_2` | The endpoint of the source/old CVAT server (for migrations). |
| `CVAT_USERNAME_2` | Admin/User for source CVAT. |
| `CVAT_PASSWORD_2` | Password for source CVAT. |
| `CVAT_SHARE_PATH` | The absolute path inside the target CVAT container for shared storage. |
| `CVAT_SHARE_PATH_2` | The absolute path inside the source CVAT container for shared storage. |

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

## 3. Exporting Annotations

Since the images already exist on your NAS (and are mounted locally), you only need to export the labels.

```bash
caah cvat project export_dataset \
  --project-id 29 \
  --no-images \
  --output-file bird_labels.zip
```

## 4. Optimized Training

Use the `--network-drive` flag to make `caah` create symbolic links to your local NAS mount instead of copying files. This saves disk space and setup time.

```bash
caah train \
  -m yolo11s \
  --data bird_labels.zip \
  --network-drive \
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

Once you have a trained model, apply it to new tasks. `caah` will attempt to read images directly from the NAS if `NAS_PATH` is configured, falling back to the CVAT API only if necessary.

```bash
caah annotate \
  --model ./runs/MTR-Bird-Model/yolo11s-640-20260306-custom/weights/best.pt \
  --task-id 123 \
  --device gpu \
  --conf 0.3 \
  --ioa 0.5
```

### Key Advantages of this Workflow
- **Zero Image Duplication**: Images stay on the NAS.
- **Speed**: Training starts instantly because no large datasets are moved or extracted.
- **Consistency**: The same image paths are used across CVAT, training, and inference.
