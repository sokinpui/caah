#!/bin/bash

set -e

caah-cmd() {
  caah --stdout "$@"
}

caah cvat project list

# Download dataset from CVAT project
echo "Input the Id of the CVAT project to export dataset from: "
read -r project_id

echo ""

echo "Input the name for the exported dataset zip ( e.g., exported_dataset.zip): "
read -r export_dataset

echo ""
echo "Exporting manual dataset from CVAT project ID $project_id to $export_dataset..."
dataset=$(caah-cmd cvat project export_dataset -u "$project_id" -o "$export_dataset" --only-manual)

echo ""
echo "Dataset exported to $dataset"

# preprocess dataset for training
echo ""
echo "Input the ratio for train and val split (e.g., 80:20): "
read -r split_ratio

echo ""
echo "Splitting dataset with ratio $split_ratio..."
train_dataset=$(caah-cmd data split -d "$dataset" -o train-datatset.zip -s "$split_ratio")

echo "Train dataset created at $train_dataset"

# train model
echo ""
echo "Input the Model version/size (e.g., yolo11n, yolo11s, yolov8m): "
read -r model_version

echo ""
echo "Input the number of epochs for training: "
read -r epochs

echo ""
echo "Input the device to use for training (cpu, gpu): "
read -r device

echo ""
echo "Input the Batch size for training: "
read -r batch_size

echo ""
echo "Input the image size for training (e.g., 640): "
read -r image_size

echo "Training model $model_version on dataset $train_dataset..."
caah-cmd train -d "$train_dataset" -m "$model_version" --epochs "$epochs" --device "$device" -b "$batch_size" --imgsz "$image_size"

# Auto annotation
echo ""
echo "Automatic annotation of new dataset"
echo "Input the path to the trained model weights (e.g., runs/train/exp/weights/best.pt): "
read -r model_path

echo ""
echo "Input the CVAT Task ID to be annotated: "
read -r task_id

echo ""
echo "Input the device to use for annotation (cpu, gpu): "
read -r device

echo ""
echo "Input the confidence threshold for annotation (e.g., 0.25): "
read -r conf_threshold

echo ""
echo "Annotating CVAT Task $task_id using model at $model_path..."
caah-cmd annotate-online -m "$model_path" --task-id "$task_id" --device "$device" --conf "$conf_threshold"

echo ""
echo "Annotation complete. Results are live in CVAT."
