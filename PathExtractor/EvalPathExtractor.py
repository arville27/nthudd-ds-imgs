from typing import List
from .PathExtractor import PathExtractor


class EvalPathExtractor(PathExtractor):
    def __init__(self, list_of_videos_path: List[str]) -> None:
        super().__init__(list_of_videos_path)

    def get_matching_label_path(self, video_path):
        path_list = video_path.split("\\")
        filename = path_list.pop()
        if "nightnoglasses" in filename:
            splitted_filename = filename.split("_")
            splitted_filename[1] = "night_noglasses"
            filename = "_".join(splitted_filename)
        complete_filename = f"{filename.split('.')[0]}ing_drowsiness.txt"

        path_list.append(complete_filename)
        complete_path = "\\".join(path_list)
        return complete_path

    def get_category(self, video_path):
        path_list = video_path.split("\\")
        filename = path_list.pop()
        if "nightnoglasses" in filename:
            return "night_noglasses"
        return filename.split("_")[1]
