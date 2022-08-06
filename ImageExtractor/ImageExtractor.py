import logging
from pathlib import Path
from typing import Dict, List
import cv2
import dlib
from Utility import Category, LabelClass
import os
import utils
import numpy as np


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

    def execute(self) -> None:
        for category in Category:
            for entry in self.__files_map[category.value]:
                self.process_entry(entry)
                utils.log_stdout(
                    f"Finish processing video {entry['video_path']}\n",
                    self.__logger.info,
                )
