# Cvat Auto Annotation Helper (`caah`)

## Requirements

- `dirnev` ( for virtual env management)

```
sudo apt install direnv
```

- `conda` (install anaconda env)

```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/sokinpui/caah.git
    cd caah
    ```

2.  Install the required dependencies(use `direnv`):
    ```bash
    conda create --name caah python=3.10
    direnv allow
    pip install -e .
    ```

For interacting with a CVAT server, create a `.env` file in the root directory of the project and add your credentials:

```bash
# Primary CVAT Server
CVAT_URL=http://localhost:8080
CVAT_USERNAME=your_username
CVAT_PASSWORD=your_password
NAS_PATH=/path/to/mount/nas
# NAS path that mount in CVAT
NAS_PREFIX=RNT

# Secondary CVAT Server (For Migration)
CVAT_URL_2=http://old-cvat:8080
CVAT_USERNAME_2=old_username
CVAT_PASSWORD_2=old_password

# Internal share paths used within CVAT containers (Migration Specifics)
CVAT_SHARE_PATH=/home/django/share/RNT
CVAT_SHARE_PATH_2=/home/django/share
```

# Usage

The tool is accessed via the `caah` command. You can explore available modules using `--help`.

```bash
caah --help
```

## Example

### 1. Export Dataset from CVAT

```bash
# YOLO 1.1 dataset with images
caah cvat project export \
  --id 26 \
  --output-dir dataset_yolo \
  --format "YOLO 1.1"

# COCO 1.0 dataset with images
caah cvat project export \
  --id 26 \
  --output-dir dataset_yolo \
  --format "COCO 1.0"

# COCO 1.0 dataset without images
caah cvat project export \
  --id 26 \
  --no-images \
  --output-dir dataset_yolo \
  --format "COCO 1.0"
```

### 2. Dataset Conversion & Slicing (SAHI)

```bash
# Convert YOLO to COCO
caah dataset yolo2coco dataset_yolo dataset_coco

# Slice images into 640x640 tiles with 20% overlap
caah dataset slice dataset_coco sliced_coco --size 640:640 --overlap 0.2:0.2

# Slice images into 640x640 tiles with 20% overlap with 40 workers
caah dataset slice dataset_coco sliced_coco --size 640:640 --overlap 0.2:0.2 -j 40

# Convert sliced COCO back to YOLO for training
caah dataset coco2yolo sliced_coco sliced_yolo
```

### 3. Training

```bash
# train with YOLO dataset
caah train \
  --data sliced_yolo \
  --model yolo11n \
  --epochs 50 \
  --imgsz 640 \
  --batch 16 \
  --device gpu \
  --workers 8 \
  --save-period 10 \
  --split 8:2 \
  --augmentation my_aug.py  # Path to .py file defining custom_transforms.
```

### 4. Auto-Annotation

```bash
caah annotate \
  --model ./weights/best.pt \
  --id 123 \
  --device gpu \
  --conf 0.25 \
  --ioa 0.5 \
  --batch 16

# with SAHI for Sliced Inference
caah annotate \
  --model ./weights/best.pt \
  --id 123 \
  --sahi \
  --size 640:640 \
  --overlap 0.2:0.2
```

---

Run with `--help/-h` to list avaliable options and commands

```
caah --help

caah -h
```
