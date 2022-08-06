import glob
import config
import json
from PathExtractor import TrainPathExtractor, EvalPathExtractor, TestPathExtractor


def execute_path_extract():
    # Train datasets
    train_videos_path = sorted(glob.glob(f"{config.RAW_TRAIN_DATASETS_PATH}/*/*/*.avi"))
    train_datasets_files = TrainPathExtractor(train_videos_path).extract_path()

    # Eval datasets
    eval_videos_path = sorted(glob.glob(f"{config.RAW_EVAL_DATASETS_PATH}/*/*.mp4"))
    eval_datasets_files = EvalPathExtractor(eval_videos_path).extract_path()

    # Test datasets
    test_videos_path = sorted(glob.glob(f"{config.RAW_TEST_DATASETS_PATH}/*.mp4"))
    test_datasets_files = TestPathExtractor(test_videos_path).extract_path()

    datasets_files = {
        "training": train_datasets_files,
        "evaluation": eval_datasets_files,
        "testing": test_datasets_files,
    }

    with open(config.DATASETS_MAPPING_FILENAME, "w") as f:
        f.write(json.dumps(datasets_files))

    print(f"Save all the datasets files path to '{config.DATASETS_MAPPING_FILENAME}'")
