import os
from os import listdir, makedirs
from os.path import isfile, join
from pathlib import Path
from typing import Dict, TypeVar, List

import numpy as np
from PIL import Image
from vidutil.encoder import VideoEncoder
from loguru import logger


TProject = TypeVar("TProject", bound="Project")


class Project:
    def __init__(self, name: str, parent_dir: Path):
        self._parent_dir = parent_dir
        self._name = name
        self._project_dir: Path = self._make_project_dir(self._name)
        self.folders: Dict[str, Project] = {}

    def _make_project_dir(self, name: str) -> Path:
        path = Path(join(self._parent_dir, name))
        makedirs(path, exist_ok=True)
        return path

    @property
    def path(self) -> Path:
        """
        Return path to directory where current Project saves artefacts
        :return:
        """
        return self._project_dir

    def get_file_names(self):
        return [
            join(self.path, f)
            for f in listdir(self.path)
            if isfile(join(self.path, f))
        ]

    def load_images(self) -> List[np.ndarray]:
        paths = VideoEncoder.list_images(self.path)
        logger.debug(f"Project path: {self.path}")
        logger.debug(f"Loading image paths: {paths}")
        return VideoEncoder.load_images(paths)

    def save_image(self, data: np.ndarray, file_name: Path):
        path = os.path.join(self.path, file_name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        im = Image.fromarray(np.uint8(data))
        im.save(path)

    def export_frames_as_video(
        self, name: str, target_project: TProject = None, fps: int=24
    ) -> None:
        """
        Exports images in current folder as a video file. You can add .mp4 as an
        extension in the name param.
        :param name: file name to export
        :return:
        """
        if target_project:
            target_path = target_project.path
        else:
            target_path = self.path

        frames = self.load_images()
        if frames:
            logger.debug(f"Video shape: {frames[0].shape[0:2]}")
        VideoEncoder.save(
            path=join(target_path, name),
            frames=frames,
            fps=fps,
            size=frames[0].shape[1::-1],  # (H,W,_) > (W,H)
        )

    def add_folder(self, name: str) -> TProject:
        folder = Project(name, parent_dir=self._project_dir)
        self.folders[name] = folder
        return folder

    def remove_folder(self, name: str) -> None:
        os.removedirs(name)
        del self.folders[name]
