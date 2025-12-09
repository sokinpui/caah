Cvat auto annotation helper

This program is a standalone tool for auto-annotating images using a trained model. It is designed to be used in conjunction with CVAT, allowing for easy import of generated annotations.

## Features

- Command-line interface for ease of use.
- Supports different annotation formats (CVAT XML, YOLO).
- Modular design for easy extension with new models or formats.
- Shell autocompletion support.

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
