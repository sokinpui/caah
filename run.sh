#!/bin/bash

caah-cmd() {
  caah --stdout "$@"
}

dataset=$(caah-cmd cvat project export_dataset -u 7 -o YOLO-dataset.zip)

echo $dataset

train_dataset=$(caah-cmd data split -d $dataset -o train-datatset.zip -s 80:20)

echo $train_dataset

caah-cmd train -d $train_dataset -m yolo11n --epochs 1 --device cpu

echo "Please enter the path to the trained model file (.pt): "
read model_path

echo "Please enter the Path to the dataset ( YOLO 1.1 format ) to annotate: "
read images_set

result=$(caah-cmd annotate -m $model_path -d $images_set -o annotated_results.zip --device cpu)

echo $result

caah cvat project import_dataset -i $result -u 7 -f yolo
