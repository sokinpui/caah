import os

import fiftyone as fo


def run_visualization():
    dataset_dir = os.path.abspath("dataset/d1")
    dataset_name = "cvat_yolo_v5"
    yaml_path = os.path.join(dataset_dir, "data.yaml")

    cleanup_existing_dataset(dataset_name)

    validate_dataset_path(yaml_path)

    dataset = load_yolo_dataset(dataset_dir, yaml_path, dataset_name)

    verify_dataset_content(dataset)

    launch_session(dataset)


def cleanup_existing_dataset(name):
    if name in fo.list_datasets():
        fo.delete_dataset(name)


def validate_dataset_path(path):
    if os.path.exists(path):
        return

    raise FileNotFoundError(
        f"Missing configuration: {path}. Ensure export is YOLOv5 format."
    )


def load_yolo_dataset(dataset_dir, yaml_path, name):
    return fo.Dataset.from_dir(
        dataset_dir=dataset_dir,
        dataset_type=fo.types.YOLOv5Dataset,
        yaml_path=yaml_path,
        name=name,
    )


def verify_dataset_content(dataset):
    if len(dataset) > 0:
        print(f"Successfully loaded {len(dataset)} samples.")
        return

    print("Warning: 0 samples loaded.")
    print("Check if the paths inside 'data.yaml' match your directory structure.")


def launch_session(dataset):
    if len(dataset) == 0:
        return

    session = fo.launch_app(dataset, remote=True, address="0.0.0.0", port=5151)
    session.wait()


if __name__ == "__main__":
    run_visualization()
