from typing import List
from .PathExtractor import PathExtractor


class TestPathExtractor(PathExtractor):
    def __init__(self, list_of_videos_path: List[str]) -> None:
        super().__init__(list_of_videos_path)

    def get_matching_label_path(self, video_path):
        path_list = video_path.split("\\")
        filename = path_list.pop()

        complete_filename = f"{filename.split('.')[0]}ing_drowsiness.txt"

        path_list.append("test_label_txt")
        path_list.append("wh")
        path_list.append(complete_filename)
        complete_path = "\\".join(path_list)
        return complete_path

    def get_category(self, video_path):
        path_list = video_path.split("\\")
        filename = path_list.pop()
        if "nightnoglasses" in filename:
            return "night_noglasses"
        return filename.split("_")[1]
