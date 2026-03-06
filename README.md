# Cvat Auto Annotation Helper (`caah`)

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

# Secondary CVAT Server (For Migration)
CVAT_URL_2=http://old-cvat:8080
CVAT_USERNAME_2=old_username
CVAT_PASSWORD_2=old_password

# NAS mapping configuration
# The prefix CVAT uses internally that should be ignored locally
NAS_PREFIX=RNT

# Internal share paths used within CVAT containers (Migration Specifics)
CVAT_SHARE_PATH=/home/django/share/RNT
CVAT_SHARE_PATH_2=/home/django/share
```

# Usage

# Usage

The tool is accessed via the `caah` command. You can explore available modules using `--help`.

```bash
caah --help
```


1.  **Dataset Management**: Export/Import projects and tasks from CVAT.
2.  **Training**: Train YOLOv11 models with NAS optimization and custom Albumentations.
3.  **Dataset Processing**: Convert between YOLO/COCO formats and perform dataset slicing (tiling) for high-resolution imagery.
4.  **Auto-Annotation**: Batch inference on CVAT tasks with IoA-based filtering of existing labels.
5.  **Migration**: Move tasks and project structures between different CVAT instances.
6.  **Upload**: Upload the result back to the same CVAT project.

## Documents
## Documents

- [Documents](./doc/README.md)
- [workflow explain](./doc/workflow/README.md)
