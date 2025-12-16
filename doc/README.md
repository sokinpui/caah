## Usage

```bash
caah --help
```

### `annotate` command

Run auto-annotation. This command has two modes:

1.  **Offline Mode**: Annotates a local dataset provided as a zip file. The input zip must contain the images.
2.  **Online Mode**: Connects to a CVAT server, annotates images from a local directory (like a network share), and uploads the results directly to a CVAT task. This is efficient as it avoids transferring image files.

#### Offline Mode Example

```bash
# Example: Annotate images and save in CVAT XML format
caah annotate --model /path/to/your/best.pt \
              --dataset /path/to/dataset.zip \
              --output /path/to/annotations.zip \
              --device cpu --conf 0.5
```

#### Online Mode Example

This is ideal for large datasets where images are stored on a shared drive and you want to update a CVAT task directly.

```bash
# Example: Annotate images for CVAT task 42
# Images are located on a mounted network drive
caah annotate --model /path/to/your/best.pt \
              --task-id 42 \
              --image-dir /mnt/shared_drive/project_images/ \
              --device cpu
```

### `train`

Train a YOLO model using a dataset in "Ultralytics YOLO" format, typically exported from CVAT as a zip file.

```bash
# Example: Train a yolo11n model for 50 epochs
caah train --data /path/to/dataset.zip \
           --model yolo11n \
           --epochs 50 \
           --device cpu
```

### `data`

Utilities for dataset manipulation, such as splitting into train/validation sets.

```bash
# Example: Split a YOLO dataset into 80% train and 20% validation
caah data split --dataset /path/to/full_dataset.zip --output /path/to/split_dataset.zip --split 80:20
```

### `convert`

Convert annotation formats from one type to another. This is useful for preparing datasets for different training frameworks.

```bash
# Example: Convert a CVAT export to YOLO format
caah convert --from cvat --to yolo --input-file cvat_export.zip --output-file yolo_dataset.zip
```

### `cvat`

Interact with a CVAT server. Make sure you have configured your `.env` file.

```bash
# List all projects
caah cvat project list

# Create a new project
caah cvat project create --name "My New Project"

# Export a project's dataset in YOLO format
# Note: Use -u for project ID
caah cvat project export_dataset -u 1 --format "YOLO 1.1" --output-file dataset_export.zip

# Import a dataset into a project (formats: yolo, cvat)
caah cvat project import_dataset -u 1 --input-file /path/to/dataset.zip --format yolo
```

### Shell Autocompletion (Optional, Recommended)

To enable shell command completion, you need to register the script with `argcomplete`.

For Bash (add to `~/.bashrc`):

```bash
eval "$(register-python-argcomplete caah)"
```

For Zsh (add to `~/.zshrc`):

```bash
# Ensure bashcompinit is loaded
autoload -U +X bashcompinit && bashcompinit
eval "$(register-python-argcomplete caah)"
```

You may need to restart your shell for the changes to take effect.

---

## Command Reference

### Global Options

- `--stdout`: Suppress all messages except the final output path to stdout.

### `annotate` command

- **Description**: Run auto-annotation (supports offline and online modes).
- **Options**:
  - `-m`, `--model` (required): Path to the YOLO model file (.pt).
  - `-d`, `--dataset`: Path to the input dataset zip file (YOLO 1.1 format). Required for offline mode.
  - `-o`, `--output`: Path for the output dataset zip file. Required for offline mode.
  - `--device`: Device to run inference on (cpu, gpu). Default: `cpu`.
  - `--conf`: Confidence threshold for predictions. Default: `0.25`.
  - `--no-mark-auto`: Disable appending ' (auto)' to class names for generated annotations.
  - `--task-id`: CVAT Task ID for online annotation. When used, `--dataset` and `--output` are ignored.
  - `--image-dir`: Local directory where task images are stored. Required for online mode.

### `convert` command

- **Description**: Convert dataset format locally.
- **Options**:
  - `-i`, `--input-file` (required): Path to input dataset zip file.
  - `-o`, `--output-file` (required): Path for the output dataset zip file.
  - `-f`, `--from` (required): Input dataset format (e.g., `CVAT`, `YOLO`, `COCO`).
  - `-t`, `--to` (required): Output dataset format (e.g., `CVAT`, `YOLO`, `COCO`).

### `cvat` command

- **Description**: Interact with a CVAT instance.
- **Subcommands**:
  - `project`
    - **Description**: Project operations.
    - **Sub-subcommands**:
      - `create`
        - **Description**: Create a project.
        - **Options**:
          - `-n`, `--name` (required): Name of the project.
      - `backup`
        - **Description**: Backup a project.
        - **Options**:
          - `-u`, `--project-id` (required): Project ID.
          - `-o`, `--output-file` (required): Path to save backup.
      - `recreate`
        - **Description**: Recreate a project from backup.
        - **Options**:
          - `-i`, `--input-file` (required): Path to backup zip.
      - `list`
        - **Description**: List projects.
      - `delete`
        - **Description**: Delete a project.
        - **Options**:
          - `-u`, `--project-id` (required): Project ID.
      - `import_dataset`
        - **Description**: Import dataset into a project.
        - **Options**:
          - `-u`, `--project-id` (required): Project ID.
          - `-i`, `--input-file` (required): Path to dataset zip file.
          - `-f`, `--format` (required): Dataset format (`yolo` or `cvat`).
      - `export_dataset`
        - **Description**: Export dataset from a project.
        - **Options**:
          - `-u`, `--project-id` (required): Project ID.
          - `-o`, `--output-file` (required): Path to save dataset.
          - `-f`, `--format`: Dataset format. Default: `YOLO 1.1`.
          - `--no-images`: Do not include images in the export.

### `data` command

- **Description**: Dataset utilities.
- **Subcommands**:
  - `split`
    - **Description**: Split a dataset into train/val sets.
    - **Options**:
      - `-d`, `--dataset` (required): Path to the input dataset zip file (YOLO 1.1 format).
      - `-o`, `--output` (required): Path for the output dataset zip file.
      - `-s`, `--split` (required): Train:Val split ratio (e.g., '80:20').
  - `unpick`
    - **Description**: Separate manual and auto annotations into different datasets.
    - **Options**:
      - `-i`, `--input` (required): Path to input mixed dataset zip.
      - `-m`, `--manual-output` (required): Path for manual output zip.
      - `-a`, `--auto-output` (required): Path for auto output zip.

### `train` command

- **Description**: Train a YOLO model.
- **Options**:
  - `-d`, `--data` (required): Path to the zipped dataset file from CVAT ('Ultralytics YOLO' format).
  - `-m`, `--model`: Model version/size (e.g., `yolo11n`, `yolo11s`, `yolov8m`). Default: `yolo11n`.
  - `-e`, `--epochs`: Number of training epochs. Default: `50`.
  - `--imgsz`: Image size (pixels). Default: `640`.
  - `-b`, `--batch`: Batch size (reduce for GPU OOM errors). Default: `16`.
  - `--device`: Device to use: '0' for GPU, 'cpu' for CPU. Default: `0`.

---

## Supported Conversion Formats

The `convert` command leverages the Datumaro library, which supports a wide range of formats. The following list includes some of the most common formats available for both input (`--from`) and output (`--to`).

- **`cifar`**: CIFAR-10/100 image classification.
- **`cityscapes`**: Urban scene segmentation.
- **`coco`**: COCO format, supporting `image_info`, `instances`, `person_keypoints`, `captions`, `labels`, `panoptic`, and `stuff`.
- **`cvat`**: Native CVAT format.
- **`imagenet`**: ImageNet classification and detection.
- **`kitti`**: KITTI format for autonomous driving, including `segmentation`, `detection`, and `3d_raw`.
- **`label_me`**: LabelMe polygon annotation format.
- **`lfw`**: Labeled Faces in the Wild, for face recognition tasks.
- **`mnist`**: MNIST handwritten digits.
- **`mots_png`**: Multi-Object Tracking and Segmentation.
- **`market1501`**: Market-1501 for person re-identification.
- **`open_images`**: Open Images Dataset.
- **`voc`**: PASCAL VOC format for `classification`, `detection`, `segmentation`, etc.
- **`tf_detection_api`**: TensorFlow Object Detection API format.
- **`vgg_face2`**: VGGFace2 face recognition dataset.
- **`wider_face`**: WIDER Face detection benchmark.
- **`yolo`**: YOLO object detection format.
