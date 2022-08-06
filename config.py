from pathlib import Path
import os

# Extract Log directory
LOG_DIR = Path("./Logs/")

# NTHU-DD Datasets root directory
RAW_NTHU_DATASETS_PATH = Path("./datasets")

# Root extract directory for images from NTHU-DD datasets
EXTRACT_DATASETS_PATH = Path("./extracted_datasets")

# Training datasets config
TRAIN_LOG_FILENAME = "training_ds.log"
RAW_TRAIN_DATASETS_PATH = RAW_NTHU_DATASETS_PATH.joinpath(
    "Training_Evaluation_Dataset", "Training Dataset"
)
EXTRACT_TRAIN_DATASETS_PATH = EXTRACT_DATASETS_PATH.joinpath("train_ds")

# Evaluation datasets config
EVAL_LOG_FILENAME = "evaluation_ds.log"
RAW_EVAL_DATASETS_PATH = RAW_NTHU_DATASETS_PATH.joinpath(
    "Training_Evaluation_Dataset", "Evaluation Dataset"
)
EXTRACT_EVAL_DATASETS_PATH = EXTRACT_DATASETS_PATH.joinpath("eval_ds")

# Testing datasets config
TEST_LOG_FILENAME = "testing_ds.log"
RAW_TEST_DATASETS_PATH = RAW_NTHU_DATASETS_PATH.joinpath("Testing_Dataset")
EXTRACT_TEST_DATASETS_PATH = EXTRACT_DATASETS_PATH.joinpath("test_ds")

# Datasets file mapping filename
# path_extractor.py will generate this file according to above configuration
# This file contain all the datasets video file pair with its label
DATASETS_MAPPING_FILENAME = "datasets_files_mapping.json"

if not RAW_NTHU_DATASETS_PATH.exists():
    print(f"'{RAW_NTHU_DATASETS_PATH}' is not exists. Exiting...")
    exit(1)
if not RAW_TRAIN_DATASETS_PATH.exists():
    print(f"'{RAW_TRAIN_DATASETS_PATH}' is not exists. Exiting...")
    exit(1)
if not RAW_EVAL_DATASETS_PATH.exists():
    print(f"'{RAW_EVAL_DATASETS_PATH}' is not exists. Exiting...")
    exit(1)
if not RAW_TEST_DATASETS_PATH.exists():
    print(f"'{RAW_TEST_DATASETS_PATH}' is not exists. Exiting...")
    exit(1)
if not LOG_DIR.exists():
    os.makedirs(LOG_DIR)
if not EXTRACT_DATASETS_PATH.exists():
    os.makedirs(EXTRACT_DATASETS_PATH)
