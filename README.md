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

## Configuration

For interacting with a CVAT server, create a `.env` file in the root directory of the project and add your credentials:

```bash
CVAT_URL=http://localhost:8080
CVAT_USERNAME=your_username
CVAT_PASSWORD=your_password
NAS_PATH=/path/to/mount/nas

CVAT_URL_2=http://old-cvat:8080
CVAT_USERNAME_2=old_username
CVAT_PASSWORD_2=old_password
```

# Usage

Run this script to use

```bash
./run.sh
```

The script will:

1. download dataset from CVAT project
2. preprocess dataset for training, spliting into train and val sets
3. train a model
4. automate annotation of a dataset
5. upload the result back to the same CVAT project
