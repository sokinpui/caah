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
# Annotate task ID 42 using a local YOLO model
caah annotate --model ./weights/best.pt --task-id 42 --device gpu --conf 0.3
```

### `cvat` command

A wrapper for interacting with the CVAT REST API.

#### Examples

```bash
# List all projects
caah cvat project list


# Export a task's dataset
caah cvat task export_dataset -tid 42 --format "YOLO 1.1" --output-file task_export.zip

# Import a dataset into a project
caah cvat project export_dataset -u 1 --format "YOLO 1.1" --output-file dataset_export.zip --only-manual

# Import a dataset into a project
caah cvat project import_dataset -u 1 --input-file /path/to/dataset.zip --format yolo
```

### `train` command

Trains a YOLO model using a zipped dataset (typically exported from CVAT).

#### Example

```bash
# Train a YOLO11n model for 100 epochs
caah train --data dataset.zip --model yolo11n --epochs 100 --device 0 --split 80:20

# Train using a custom local model as base
caah train --data dataset.zip --path ./weights/best.pt --epochs 50
```

### `convert` command

Converts local datasets between different formats using Datumaro.

#### Example

```bash
# Convert CVAT XML to YOLO format
caah convert -i input.zip -o output.zip --from cvat --to yolo
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
  - `-s`, `--split`: Ratio to split dataset if not already split.

### `convert` command

- **Description**: Convert dataset format locally.
- **Options**:
  - `-i`, `--input-file` (required): Path to source zip.
  - `-o`, `--output-file` (required): Path for output zip.
  - `-f`, `--from` (required): Source format (e.g., cvat, coco).
  - `-t`, `--to` (required): Destination format (e.g., yolo, voc).
