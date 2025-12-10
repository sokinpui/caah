# Cvat Auto Annotation Helper (`caah`)

This program is a standalone tool for auto-annotating images using a trained model. It is designed to be used in conjunction with CVAT, allowing for easy import of generated annotations.
It also includes utilities for training models, converting dataset formats, and interacting with a CVAT instance via its REST API.

## Features

- **Auto-annotation**: Predict bounding boxes on a set of images using a trained YOLO model.
- **Model Training**: Train a YOLO model with a dataset exported from CVAT.
- **Dataset Conversion**: Convert annotation formats between different types (e.g., CVAT to YOLO) locally.
- **CVAT Integration**: A command-line client to interact with a CVAT server's REST API for managing projects.
- **Command-line interface**: Easy to use and scriptable.
- **Shell Autocompletion**: Supports `argcomplete` for easy command discovery.

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/sokinpui/caah.git
    cd caah
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

For interacting with a CVAT server, create a `.env` file in the root directory of the project and add your credentials:

```CVAT_URL=http://localhost:8080
CVAT_USERNAME=your_username
CVAT_PASSWORD=your_password```

## Usage

The tool is organized into several commands. You can see all available commands by running:

```bash
caah --help
```

### `annotate`

Automatically generate annotations for a dataset.

```bash
# Example: Annotate images and save in CVAT XML format
caah annotate --model /path/to/your/best.pt \
              --dataset /path/to/dataset.zip \
              --output /path/to/annotations.zip \
              --device cpu --conf 0.5
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

````bash
# Ensure bashcompinit is loaded
autoload -U +X bashcompinit && bashcompinit
eval "$(register-python-argcomplete caah)"
    ```

You may need to restart your shell for the changes to take effect.
