Cvat auto annotation helper

This program is a standalone tool for auto-annotating images using a trained model. It is designed to be used in conjunction with CVAT, allowing for easy import of generated annotations.

## Features

-   Command-line interface for ease of use.
-   Supports different annotation formats (CVAT XML, YOLO).
-   Modular design for easy extension with new models or formats.
-   Shell autocompletion support.

## Usage

1.  **Installation**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Enable Autocompletion (Optional, Recommended)**

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

3.  **Running the annotation**

    ```bash
    python src/main.py --model <path_to_model> --images <path_to_images_dir> --output <path_to_output_dir> --output-format <format>
    ```

### Arguments

-   `--model`: Path to the trained YOLO model file (e.g., a `.pt` file).
-   `--images`: Path to the directory containing images to be annotated.
-   `--output`: Path to the directory where annotation files will be saved.
-   `--output-format`: The desired output format for annotations. Supported formats are `cvat` (default) and `yolo`.
-   `--copy`: If provided, copies the original images to the output directory.
-   `--device`: Device to run the model on. Supported formats are `gpu` (default) and `cpu`.

### Example

```bash
# Create dummy files for demonstration
touch dummy_model.pth
mkdir -p images_to_annotate output_annotations
touch images_to_annotate/image1.jpg
touch images_to_annotate/image2.png

# Run the annotation process
python src/main.py --model dummy_model.pth --images images_to_annotate --output output_annotations --output-format cvat --copy
```

This will generate an `annotations.xml` file in the `output_annotations` directory, which can then be uploaded to a CVAT task.

If you use `--output-format yolo`, it will create a `.txt` file for each image in the output directory.
