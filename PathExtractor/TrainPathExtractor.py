from typing import List
from .PathExtractor import PathExtractor


class TrainPathExtractor(PathExtractor):
    def __init__(self, list_of_videos_path: List[str]) -> None:
        super().__init__(list_of_videos_path)

    def get_matching_label_path(self, video_path):
        path_list = video_path.split("\\")
        filename = path_list.pop()
        folder = path_list[-2]
        complete_filename = f"{folder}_{filename.split('.')[0]}_drowsiness.txt"

        path_list.append(complete_filename)
        complete_path = "\\".join(path_list)
        return complete_path

    def get_category(self, video_path):
        path_list = video_path.split("\\")
        category = path_list[-2]
        return category
