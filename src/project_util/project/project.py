import os
from os import listdir, makedirs
from os.path import isfile, join
from pathlib import Path
from typing import Dict, TypeVar, List, Union

import numpy as np
from PIL import Image
from vidutil.encoder import VideoEncoder
from loguru import logger

from project_util.constants import FILE_SYSTEM
from project_util.services.s3 import S3Client

TProject = TypeVar("TProject", bound="Project")


class Project:
    def __init__(self, name: str, parent_dir: Path, backend: str = FILE_SYSTEM):
        self._parent_dir = parent_dir
        self._name = name
        self._project_dir: Path = self._make_project_dir(self._name)
        self.folders: Dict[str, Project] = {}
        self._s3_client = None
        self._backend = backend

    @property
    def s3_client(self):
        if not self._s3_client:
            self._s3_client = S3Client()
        return self._s3_client

    def dir_of_file(self, file, parents: int):
        """Return the abs path of a __file__ variable"""
        # todo: implement

    def _make_project_dir(self, name: str) -> Path:
        path = Path(join(self._parent_dir, name)).absolute()
        makedirs(path, exist_ok=True)
        return path

    @property
    def path(self) -> Path:
        """
        Return path to directory where current Project saves artefacts
        :return:
        """
        return self._project_dir

    def create_file_name(self, name: str) -> str:
        """
        Create a filename relative to the current project directory
        :param name:
        :return:
        """
        return os.path.join(self._project_dir, name)

    def get_file_names(self):
        """
        Get all filenames in current project directory
        :return:
        """
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

    def save_image(
        self,
        data: np.ndarray,
        file_name: Path,
    ) -> str:
        path = os.path.join(self.path, file_name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        im = Image.fromarray(np.uint8(data))
        im.save(path)
        return os.path.abspath(path)

    def save_image_to_s3(self, data: np.ndarray, bucket: str, path: str) -> str:
        im = Image.fromarray(np.uint8(data))
        result = self.s3_client.save(
            data=im.tobytes(),
            bucket=bucket,
            path=path,
        )
        return result.get("ETag")

    def export_frames_as_video(
        self,
        name: str,
        target_project: TProject = None,
        fps: int = 24,
        codec: Union[str, int] = "mp4v",
    ) -> None:
        """
        Exports images in current folder as a video file. You can add .mp4 as an
        extension in the name param.
        :param codec: fourcc code
        :param name: file name to export
        :return:
        """
        if target_project:
            target_path = target_project.path
        else:
            target_path = self.path

        frames = self.load_images()
        if frames:
            logger.debug(f"Video shape: {frames[0].shape[1::-1]}")
        VideoEncoder.save(
            path=join(target_path, name),
            frames=frames,
            fps=fps,
            codec=codec,
        )

    def add_folder(self, name: str) -> TProject:
        folder = Project(name, parent_dir=self._project_dir)
        self.folders[name] = folder
        return folder

    def remove_folder(self, name: str) -> None:
        # todo: use abspath
        os.removedirs(name)
        del self.folders[name]
