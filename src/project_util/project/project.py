import io
import os
from os import listdir, makedirs
from os.path import isfile, join
from pathlib import Path
from typing import Dict, List, Optional, TypeVar, Union

import numpy as np
from loguru import logger
from PIL import Image
from vidutil.encoder import VideoEncoder

from project_util.constants import FILE_SYSTEM, S3
from project_util.services.s3 import S3Client


TProject = TypeVar("TProject", bound="Project")


class Project:
    def __init__(self, name: str, parent_dir: Path, backend: str = FILE_SYSTEM):
        self._backend = backend
        self._parent_dir = parent_dir
        self._name = name
        self._project_dir: Path = self._make_project_dir(self._name)
        self.folders: Dict[str, Project] = {}
        self._s3_client = None

    @property
    def s3_client(self):
        if not self._s3_client:
            self._s3_client = S3Client()
        return self._s3_client

    def dir_of_file(self, file, parents: int):
        """Return the abs path of a __file__ variable"""
        # todo: implement

    def _make_project_dir(self, name: str) -> Path:
        if self._backend == FILE_SYSTEM:
            path = Path(join(self._parent_dir, name)).absolute()
            makedirs(path, exist_ok=True)
        elif self._backend == S3:
            path = Path(join(self._parent_dir, name))
        else:
            raise ValueError(f"Unsupported backend: {self._backend}")
        return path

    @property
    def path(self) -> Path:
        """
        Return path to directory where current Project saves artefacts
        :return:
        """
        return self._project_dir

    @property
    def backend(self):
        return self._backend

    def create_file_name(self, name: str) -> str:
        """
        Create a filename relative to the current project directory.
        Just an implementation of os.path.join() for the current project dir.
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
        # Candidate for moving to an image-specific project lib
        paths = VideoEncoder.list_images(self.path)
        logger.debug(f"Project path: {self.path}")
        logger.debug(f"Loading image paths: {paths}")
        return VideoEncoder.load_images(paths)

    def _require_backend(self, backend):
        if self._backend != backend:
            raise RuntimeError(
                f"operation is only supported on backend {backend}"
            )

    def save_image(
        self,
        data: np.ndarray,
        file_name: Union[str, Path],
        bucket: Optional[str] = None,
        img_format: str = "PNG",
    ) -> Union[Path, str]:
        # Candidate for moving to an image-specific project lib
        if isinstance(file_name, Path):
            file_name = file_name.as_posix()
        if self._backend == S3:
            if not bucket:
                raise ValueError(
                    "bucket and path are required for saving to S3"
                )
            return self._save_image_to_s3(
                data=data,
                bucket=bucket,
                path=file_name,
                img_format=img_format,
            )
        elif self._backend == FILE_SYSTEM:
            return self._save_image_to_file_system(
                data, file_name, img_format=img_format
            )
        else:
            raise ValueError(f"{self._backend} not supported")

    def _save_image_to_file_system(
        self, data: np.ndarray, file_name: Union[str, Path], img_format: str
    ) -> str:
        # Candidate for moving to an image-specific project lib
        path = os.path.join(self.path, file_name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        im = Image.fromarray(np.uint8(data))
        im.save(path, format=img_format)
        return os.path.abspath(path)

    def _save_image_to_s3(
        self,
        data: np.ndarray,
        bucket: str,
        path: str,
        img_format: str,
    ) -> str:
        # Candidate for moving to an image-specific project lib
        im = Image.fromarray(np.uint8(data))
        im_bytes = io.BytesIO()
        im.save(im_bytes, format=img_format)

        result = self.s3_client.save(
            data=im_bytes.getvalue(),
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
        # Candidate for moving to a video-specific project lib
        self._require_backend(FILE_SYSTEM)
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
        folder = Project(
            name, parent_dir=self._project_dir, backend=self._backend
        )
        self.folders[name] = folder
        return folder

    def remove_folder(self, name: str) -> None:
        # todo: use abspath
        if self._backend == FILE_SYSTEM:
            os.removedirs(self.path.joinpath(name))
        del self.folders[name]
