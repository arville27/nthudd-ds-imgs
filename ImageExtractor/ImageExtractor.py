import logging
from pathlib import Path
from typing import Dict, List, Tuple
import cv2
import dlib
from Utility import Category, LabelClass
import os
import utils
import numpy as np
import re


class ImageExtractor:
    def __init__(
        self,
        logger: logging.Logger,
        total_processed_frame: int,
        files_map: List[str],
        extract_target_path: str | Path,
    ) -> None:
        self.__detector = dlib.get_frontal_face_detector()
        self.__total_processed_frame = total_processed_frame
        self.__logger = logger
        self.__files_map = files_map
        self.__extract_target_path = Path(extract_target_path)
        self.__extract_target_path_awake = self.__extract_target_path.joinpath("awake")
        self.__extract_target_path_drowsy = self.__extract_target_path.joinpath(
            "drowsy"
        )

        if not self.__extract_target_path.exists():
            os.makedirs(self.__extract_target_path)
            os.makedirs(self.__extract_target_path_awake)
            os.makedirs(self.__extract_target_path_drowsy)

    def get_total_processed_frame(self) -> int:
        return self.__total_processed_frame

    def process_image(self, frame):
        # transform the BGR frame in grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # apply a bilateral filter to lower noise but keep frame details
        gray = cv2.bilateralFilter(gray, 5, 10, 10)

        # Face detection
        faces = self.__detector(gray)

        if len(faces) > 0:
            face = faces[0]

            (x1, y1) = (face.left(), face.top())
            (x2, y2) = (face.right(), face.bottom())

            # Crop frame to face area
            frame = frame[y1:y2, x1:x2]

            return True, frame
        return False, None

    def save_frame(self, frame: np.ndarray, filename: str | Path) -> bool:
        try:
            cv2.imwrite(str(filename), frame)
            return True, None
        except Exception as e:
            return False, e

    def process_entry(self, entry: Dict) -> None:
        cv2.setUseOptimized(True)

        video_path = entry["video_path"]
        label_path = entry["label_path"]

        video = cv2.VideoCapture(video_path)
        label = utils.read_file(label_path)

        if not video.isOpened():
            utils.log_stdout(f"Cannot open file {video_path}", self.__logger.error)
            exit()

        frame_count = 0

        while video.isOpened():
            ret, image = video.read()

            if not ret:
                break

            # Apply filter, get face area, and crop it
            is_success, final_img = self.process_image(image)

            if not is_success:
                utils.log_stdout(
                    f"Cannot extract face from video {video_path} on frame {frame_count}",
                    self.__logger.error,
                )
                self.__total_processed_frame += 1
                frame_count += 1
                continue

            try:
                label_value = label[frame_count]
            except IndexError:
                utils.log_stdout(
                    f"Label value is not available for video {video_path} for frame {frame_count}. Please verify that label file length is the same with the amount of frames in the video",
                    self.__logger.error,
                )
                exit(1)
            if LabelClass(int(label_value)) == LabelClass.AWAKE:
                filename = self.__extract_target_path_awake.joinpath(
                    f"{self.__total_processed_frame}.jpg"
                )
            elif LabelClass(int(label_value)) == LabelClass.DROWSY:
                filename = self.__extract_target_path_drowsy.joinpath(
                    f"{self.__total_processed_frame}.jpg"
                )
            else:
                utils.log_stdout(
                    f"Unknown class label with value of {label[frame_count]}. For video {video_path} in frame {frame_count}",
                    self.__logger.error,
                )

            status, error = self.save_frame(final_img, filename)
            if not status:
                utils.log_stdout(
                    f"Cannot save frame to file. Video {video_path} on frame {frame_count}. With error:\n{error}",
                    self.__logger.error,
                )

            frame_count += 1
            self.__total_processed_frame += 1

            if self.__total_processed_frame % 100 == 0:
                utils.log_stdout(
                    f"Processed {self.__total_processed_frame} total frames",
                    self.__logger.info,
                )

    def check_entry(self, entry) -> Tuple[bool, int, int]:
        video_path = entry["video_path"]
        label_path = entry["label_path"]

        cap = cv2.VideoCapture(video_path)

        label_count = int(len(utils.read_file(label_path)))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return (frame_count == label_count, frame_count, label_count)

    def populate_missing_label_val(self, entry, frame_count, label_count) -> None:
        label_path = entry["label_path"]
        label_content = utils.read_file(label_path)

        missing_value_count = frame_count - label_count
        if missing_value_count > 0 and missing_value_count < 4:
            utils.log_stdout(
                f"Automatically infer missing value by its last value, because missing value is less than 4\n",
                self.__logger.info,
            )
            label_content += label_content[label_count - 1] * missing_value_count
        elif missing_value_count > 0:
            status = True
            while status:
                user_inputed_missing_val = input(
                    f"Enter {missing_value_count} digits (0,1), each digit is representing label for corresponding frame"
                )
                if (
                    len(user_inputed_missing_val) > missing_value_count
                    or re.match(r"^[^2-9A-z]+$", user_inputed_missing_val) is None
                ):
                    print(
                        f"Please input {missing_value_count} digits characters, consisting only 1 and 0"
                    )
                    continue
                status = False
            label_content += user_inputed_missing_val
            utils.log_stdout(
                f"Succesfully append missing value in {label_path} file with user inputed characters ({user_inputed_missing_val})\n",
                self.__logger.info,
            )
        utils.write_file(label_path, label_content)

    def check_label_completion(self, populate_missing_val: bool) -> None:
        all_match = True
        for category in Category:
            for entry in self.__files_map.get(category.value):
                match_status, frame_count, label_count = self.check_entry(entry)
                if all_match and not match_status:
                    utils.log_stdout(
                        "There are one or more entries that cannot be processed due to an error in the number of frames and labels",
                        self.__logger.error,
                    )
                    all_match = False
                if not match_status:
                    utils.log_stdout(
                        f"Video {entry['video_path']}, Label {entry['label_path']}\nWith frame count: {frame_count}\nLabel count: {label_count}",
                        self.__logger.error,
                    )
                    if populate_missing_val:
                        if frame_count - label_count > 0:
                            self.populate_missing_label_val(
                                entry, frame_count, label_count
                            )
                        else:
                            utils.log_stdout(
                                "Please manually verify the label content\n",
                                self.__logger.warn,
                            )
                    else:
                        utils.log_stdout("", self.__logger.info)
        return all_match

    def execute(self) -> None:
        for category in Category:
            for entry in self.__files_map[category.value]:
                self.process_entry(entry)
                utils.log_stdout(
                    f"Finish processing video {entry['video_path']}\n",
                    self.__logger.info,
                )
