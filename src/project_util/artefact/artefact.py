import os.path
from functools import lru_cache
from pathlib import Path
from typing import Optional, Tuple, TypeVar

import cv2
import numpy as np
from cv2 import dnn_superres
from PIL import Image

from project_util.naming.naming import NamingUtil
from project_util.project.project import Project

TArtefact = TypeVar("TArtefact", bound="Artefact")


class Artefact:
    def __init__(
        self,
        name: str,
        project: Optional[Project] = None,
        size: Optional[Tuple[int, int]] = None,
        data: Optional[np.ndarray] = None,
    ):
        if data is None and size is None:
            raise ValueError("Data or size should be defined")
        self.name = name
        self.project = project
        self.data = data  # when in color, should always be RGB(A)
        self.size = size
        if data is not None:
            self._update_size()
        else:
            self.fill((0, 0, 0))

    def _update_size(self):
        self.size = self.data.shape[0], self.data.shape[1]

    @property
    def width(self):
        return self.size[0] if self.size else None

    @property
    def height(self):
        return self.size[1] if self.size else None

    def update(self, data: np.ndarray):
        self.data = data
        self._update_size()

    def get_superres(
        self,
        upscale: int = 4,
        new_name: Optional[str] = None,
        new_project: Optional[Project] = None,
    ) -> TArtefact:
        """
        Return a version of the current artefact in an AI-upsampled resolution
        :param project:
        :param new_name:
        :param upscale:
        :return:
        """
        if upscale not in (2, 3, 4):
            raise ValueError("Upscale should be 2, 3, or 4")
        superres = self.get_superres_ml_model(upscale)
        return Artefact(
            name=new_name or NamingUtil.insert_suffix(self.name, suffix=f"@x{upscale}"),
            data=superres.upsample(self.data),
            project=new_project or self.project,
        )

    @staticmethod
    @lru_cache
    def get_superres_ml_model(upscale):
        sr = dnn_superres.DnnSuperResImpl_create()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, f"ml-models/EDSR_x{upscale}.pb")
        sr.readModel(model_path)
        # Set the desired model and scale to get correct pre- and post-processing
        sr.setModel("edsr", upscale)
        return sr

    @staticmethod
    def cv2_to_pil(data: np.ndarray) -> Image:
        return Image.fromarray(cv2.cvtColor(data, cv2.COLOR_BGR2RGB))

    @staticmethod
    def pil_to_cv2(img: Image) -> np.ndarray:
        pil_as_arr = np.array(img)
        return cv2.cvtColor(pil_as_arr, cv2.COLOR_RGB2BGR)

    def save(
        self, project: Optional[Project] = None, suffix: Optional[str] = None
    ) -> None:
        """
        Save this artefact into a project
        :param project: a Project instance
        :param suffix: suffix to insert into the file name. For example,
                        if the suffix is @3x and the artefact name is icon.png,
                        then the filename becomes icon@3x.png.
        :return:
        """
        if not project:
            project = self.project
        file_name = NamingUtil.insert_suffix(self.name, suffix)
        project.save_image(data=self.data, file_name=Path(file_name))

    def fill(self, rgb: Tuple) -> None:
        image: Image = Image.new("RGB", self.size)
        image.paste(rgb, [0, 0, self.width, self.height])
        self.data = np.array(image)
