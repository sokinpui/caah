#!/bin/bash

set -e

# ==========================================
# CONFIGURATION
# ==========================================
# Set to "task" or "project"
EXPORT_TYPE="task"
IDS="160 57 56"
OUTPUT_ROOT="dataset"
# ==========================================

if [ -z "$IDS" ]; then
  exit 1
fi

ID_CSV=$(echo "$IDS" | tr ' ' ',')
SAFE_NAME=$(echo "$ID_CSV" | tr ',' '_')

BASE_DIR="${OUTPUT_ROOT}/${EXPORT_TYPE}_${SAFE_NAME}"
EXPORT_DIR="${BASE_DIR}/export"
FILTER_DIR="${BASE_DIR}/filtered"
DOWNLOAD_DIR="${BASE_DIR}/download"
SLICE_DIR="${BASE_DIR}/slice"
YOLO_DIR="${BASE_DIR}/yolo"

mkdir -p "$BASE_DIR"

if [ "$EXPORT_TYPE" == "project" ]; then
  echo "[1/5] Exporting project(s): ${ID_CSV}..."
  caah cvat project export -o "$EXPORT_DIR" --id "$ID_CSV" -f "COCO 1.0" --no-images
  echo
elif [ "$EXPORT_TYPE" == "task" ]; then
  echo "[1/5] Exporting task(s): ${ID_CSV}..."
  caah cvat task export -o "$EXPORT_DIR" --ids "$ID_CSV" -f "COCO 1.0" --no-images
  echo
else
  echo "Error: EXPORT_TYPE must be either 'task' or 'project'. Current value: $EXPORT_TYPE"
  exit 1
fi

echo "[2/5] Filtering unannotated images..."
caah dataset filter "$EXPORT_DIR" "$FILTER_DIR"
echo

echo "[3/5] Downloading images from NAS..."
caah dataset download "$FILTER_DIR" "$DOWNLOAD_DIR"
echo

echo "[4/5] Slicing dataset into patches..."
caah dataset slice "$DOWNLOAD_DIR" "$SLICE_DIR"
echo

echo "[5/5] Converting final dataset to YOLO format..."
caah dataset coco2yolo "$SLICE_DIR" "$YOLO_DIR"
echo

echo "------------------------------------------------"
echo "Pipeline complete!"
echo "Final YOLO dataset location: $YOLO_DIR"
