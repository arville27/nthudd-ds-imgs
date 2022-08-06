from Utility import Logger
import path_extractor
import config
import utils
import argparse
from ImageExtractor import ImageExtractor
from pathlib import Path


def main(args):
    if args.execute_path_extract:
        path_extractor.execute_path_extract()

    if not Path(config.DATASETS_MAPPING_FILENAME).exists():
        print(
            f"'{config.DATASETS_MAPPING_FILENAME}' is not exists. Try running with --execute-path-extract switch. Exiting..."
        )
        exit(1)

    type = args.datasets_type
    files_map = utils.read_json(config.DATASETS_MAPPING_FILENAME).get(type)
    if type == "training":
        logger = Logger.get_logger(config.TRAIN_LOG_FILENAME)
        extract_target_path = config.EXTRACT_TRAIN_DATASETS_PATH
    elif type == "evaluation":
        logger = Logger.get_logger(config.EVAL_LOG_FILENAME)
        extract_target_path = config.EXTRACT_EVAL_DATASETS_PATH
    elif type == "testing":
        logger = Logger.get_logger(config.TEST_LOG_FILENAME)
        extract_target_path = config.EXTRACT_TEST_DATASETS_PATH

    if files_map is None:
        print(
            f"{type} datasets files mapping not found in {config.DATASETS_MAPPING_FILENAME}"
        )
        exit(1)

    ImageExtractor(
        logger=logger,
        total_processed_frame=0,
        files_map=files_map,
        extract_target_path=extract_target_path,
    ).execute()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NTHU-DD Datasets preprocessor")

    parser.add_argument(
        "datasets_type",
        choices=["training", "evaluation", "testing"],
        help="Datasets type to extract images from",
    )

    parser.add_argument(
        "--execute-path-extract",
        action="store_true",
        help="Execute path_extractor before process datasets",
    )

    args = parser.parse_args()
    main(args)
