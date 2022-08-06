from typing import List
from abc import ABC, abstractmethod
from pathlib import Path


class PathExtractor(ABC):
    def __init__(self, list_of_videos_path: List[str]) -> None:
        self.videos = list_of_videos_path

    def extract_path(self):
        locations = {}
        for video_path in self.videos:
            label_path = self.get_matching_label_path(video_path)
            category = self.get_category(video_path)
            entry = {
                "video_path": video_path,
                "label_path": label_path,
            }

            if not Path(entry["video_path"]).exists():
                raise Exception(f"{Path(entry['video_path'])} is not exists")
            if not Path(entry["label_path"]).exists():
                raise Exception(f"{Path(entry['label_path'])} is not exists")

            category_list = locations.get(category)
            if category_list is None:
                locations[category] = []
            locations[category].append(entry)

        return locations

    @abstractmethod
    def get_matching_label_path(self, video_path):
        pass

    @abstractmethod
    def get_category(self, video_path):
        pass
