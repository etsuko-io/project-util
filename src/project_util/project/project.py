import os
from os import listdir, makedirs
from os.path import isfile, join
from pathlib import Path
from typing import Dict, TypeVar

import numpy as np
from PIL import Image
from vidutil.encoder import VideoEncoder

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

    def save_image(self, data: np.ndarray, file_name: Path):
        path = os.path.join(self.path, file_name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        im = Image.fromarray(np.uint8(data))
        im.save(path)

    def export_frames_as_video(self, name: str) -> None:
        """
        Exports images in current folder as a video file. You can add .mp4 as an
        extension in the name param.
        :param name: file name to export
        :return:
        """
        paths = VideoEncoder.list_images(self.path)
        frames = VideoEncoder.load_images(paths)
        VideoEncoder.save(
            path=join(self.path, name),
            frames=frames,
            fps=24,
            size=frames[0].shape[0:2],
        )

    def add_folder(self, name: str) -> TProject:
        folder = Project(name, parent_dir=self._project_dir)
        self.folders[name] = folder
        return folder
