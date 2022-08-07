import logging
from pathlib import Path
from typing import List
from Utility import Category
import os
import utils
from ImageExtractor import ImageExtractor


class TestingImageExtractor(ImageExtractor):
    def __init__(
        self,
        logger: logging.Logger,
        total_processed_frame: int,
        files_map: List[str],
        extract_target_path: str | Path,
    ) -> None:
        super().__init__(logger, total_processed_frame, files_map, extract_target_path)
        if extract_target_path.joinpath("awake").exists():
            os.removedirs(extract_target_path.joinpath("awake"))
        if extract_target_path.joinpath("drowsy").exists():
            os.removedirs(extract_target_path.joinpath("drowsy"))
        for category in Category:
            root_category_dir = extract_target_path.joinpath(category.value)
            if not root_category_dir.exists():
                os.makedirs(root_category_dir)
            if not root_category_dir.joinpath("awake").exists():
                os.makedirs(root_category_dir.joinpath("awake"))
            if not root_category_dir.joinpath("drowsy").exists():
                os.makedirs(root_category_dir.joinpath("drowsy"))

    def execute(self) -> None:
        for category in Category:
            self._ImageExtractor__extract_target_path_awake = (
                self._ImageExtractor__extract_target_path.joinpath(
                    category.value, "awake"
                )
            )
            self._ImageExtractor__extract_target_path_drowsy = (
                self._ImageExtractor__extract_target_path.joinpath(
                    category.value, "drowsy"
                )
            )
            for entry in self._ImageExtractor__files_map[category.value]:
                self.process_entry(entry)
                utils.log_stdout(
                    f"Finish processing video {entry['video_path']}\n",
                    self._ImageExtractor__logger.info,
                )
