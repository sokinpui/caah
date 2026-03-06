# CAAH Documentation

## Basic Usage

To see all available commands and global options, run:

```bash
caah --help
```

### `annotate` command

Connects to a CVAT server, performs inference on task frames using a YOLO model, and uploads the results directly as annotations.

#### Example

```bash
# Annotate task ID 42 using a local YOLO model with 16-frame batching
caah annotate --model ./weights/best.pt --task-id 42 --device gpu --conf 0.3
```

### `cvat` command

A wrapper for interacting with the CVAT REST API.

```bash
# List all projects
caah cvat project list
# Import a project from a backup
caah cvat project import my_project_backup.zip

# Import a dataset into a project
caah cvat project import_dataset -u 1 --input-file /path/to/dataset.zip --format yolo
```

#### Project Management
```bash
# Create a new project
caah cvat project create "New Project Name"

# Backup a project to a zip file
caah cvat project backup --project-id 1 --output-file backup.zip
```

### `dataset` command

Utilities for format conversion and image tiling.

```bash
# Convert YOLO export to COCO (required for slicing)
caah dataset yolo2coco input_yolo.zip output_coco.zip

# Slice a COCO dataset into 640x640 tiles with 20% overlap
caah dataset slice input_coco.zip sliced_coco.zip --size 640:640 --overlap 0.2:0.2

# Convert sliced COCO back to YOLO for training
caah dataset coco2yolo sliced_coco.zip sliced_yolo.zip
```


### `train` command

Trains a YOLO model using a zipped dataset (typically exported from CVAT).

#### Example

```bash
# Train with custom augmentations and NAS optimization
caah train --data labels_only.zip --network-drive --split 8:2 --augmentation ./my_aug.py --project "Bird-Detection" --name "YOLO11s-v1"
```

---


If your images are stored on a NAS and mapped in CVAT as "Share" storage, use this workflow to avoid downloading massive datasets:

1.  **Export Labels**: `caah cvat project export_dataset --project-id 1 --no-images --output-file labels.zip`
2.  **Train**: `caah train --data labels.zip --network-drive --split 8:2`

*Note: This creates symlinks to the NAS images instead of copying them to the local machine.*

---

### `migrate` command
### `migrate` command

Tools for moving projects and tasks between different CVAT servers (uses `CVAT_URL_2` etc. in `.env`).

#### Example

```bash
# Migrate a specific task and remap NAS paths
caah migrate task --task-id 123 --old-prefix /mnt/old/share --new-prefix /home/django/share

# Sync all project structures and labels from source to target server
caah migrate project-layout
```

---

## Command Reference

### Global Options

- `--stdout`: Suppress all messages except the final output path to stdout.

- **Resource**: `task`
  - **Action**: `export_dataset`
    - **Description**: Export all annotations and images from a task.
    - **Options**:
      - `-tid`, `--task-id` (required): ID of the task.
      - `-o`, `--output-file` (required): Path to save dataset.
      - `-f`, `--format`: Dataset format. Default: `YOLO 1.1`.
      - `--no-images`: Do not include images in the export.
      - `--only-manual`: Export only manual annotations.

- **Resource**: `project`
  - **Action**: `list`
    - **Description**: List all projects in the CVAT instance.
  - **Action**: `create`
    - **Options**:
      - `-n`, `--name` (required): Project name.
  - **Action**: `delete`
    - **Options**:
      - `-u`, `--project-id` (required): ID of the project to delete.
  - **Action**: `export_dataset`
    - **Description**: Export all annotations and images from a project.
    - **Options**:
      - `-u`, `--project-id` (required): ID of the project.
      - `-o`, `--output-file` (required): Path to save dataset.
      - `-f`, `--format`: Dataset format. Default: `YOLO 1.1`.
      - `--no-images`: Do not include images in the export.
      - `--only-manual`: Export only manual annotations.

### `train` command

- **Description**: Train a YOLO model.
- **Options**:
  - `-d`, `--data` (required): Path to the zipped dataset file.
  - `-m`, `--model`: YOLO model version (e.g., yolo11n). Default: `yolo11n`.
  - `-p`, `--path`: Path to a custom local model file (.pt).
  - `-e`, `--epochs`: Number of training epochs. Default: `50`.
  - `--imgsz`: Input image size. Default: `640`.
  - `-b`, `--batch`: Batch size. Default: `16`.
  - `--device`: Training device (cpu, gpu, or ID). Default: `gpu`.
  - `-s`, `--split`: Ratio to split dataset (e.g., 8:2).
  - `--project`: Project name for experiment tracking.
  - `--name`: Name of the specific training run.
  - `--save-period`: Save a checkpoint every X epochs.
  - `--workers`: Number of data loader workers. Default: `8`.
  - `--network-drive`: Enable NAS optimization (requires `NAS_PATH` in `.env`).
  - `-a`, `--augmentation`: Path to a Python file defining `custom_transforms` (Albumentations).

  - **Action**: `backup`
    - **Description**: Export a project backup file.
    - **Options**:
      - `-u`, `--project-id`: ID of the project.
      - `-o`, `--output-file`: Path to save the backup zip.
  - **Action**: `import`
    - **Description**: Import a project from a backup file.
    - **Options**:
      - `-i`, `--input-file`: Path to the backup zip.

### `migrate` command

- **Action**: `task`
  - **Description**: Migrate a single task using NAS share optimization.
  - **Options**:
    - `-t`, `--task-id`: Source task ID.
    - `-p`, `--project-id`: Target project ID (optional).
    - `--old-prefix`: Prefix to replace in source file paths.
    - `--new-prefix`: New prefix for target file paths.

- **Action**: `tasks`
  - **Description**: Bulk migrate all tasks, matching projects by name.
  - **Options**:
    - `--orphans`: Migrate tasks not assigned to any project.
    - `-j`, `--jobs`: Parallel migration workers.
    - `--old-prefix`: Prefix to replace in source file paths.
    - `--new-prefix`: New prefix for target file paths.

- **Action**: `project-layout`
  - **Description**: Recreate project structures (names and labels) on the target server.
  - **Options**:
    - `-p`, `--project-id`: Specific project to sync (if omitted, syncs all).

### `annotate` command

- **Description**: Perform auto-annotation on a CVAT task.
- **Options**:
  - `-m`, `--model` (required): Path to model.
  - `--task-id` (required): CVAT Task ID.
  - `--device`: cpu or gpu.
  - `--conf`: Confidence threshold (0.0-1.0).
  - `--ioa`: IoA threshold to filter existing annotations.
  - `--jobs`: Parallel workers for image fetching.
  - `--batch`: Inference batch size.
