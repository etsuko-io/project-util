import os.path
from functools import lru_cache
from pathlib import Path
from typing import Optional, Tuple, TypeVar

import cv2
import numpy as np
from cv2 import dnn_superres
from PIL import Image

from project.project import Project

TArtefact = TypeVar("TArtefact", bound="Artefact")


class Artefact:
    def __init__(
        self,
        name: str,
        size: Optional[Tuple[int, int]] = None,
        data: Optional[np.ndarray] = None,
    ):
        if data is None and size is None:
            raise ValueError("Data or size should be defined")
        self.name = name
        self.data = data  # when in color, should always be RGB(A)
        self.size = size
        if self.size:
            self.width = size[0]
            self.height = size[1]
        if data is not None:
            self._update_size()
        else:
            self.fill((0, 0, 0))

    def _update_size(self):
        self.size = self.data.shape[0], self.data.shape[1]

    def update(self, data: np.ndarray):
        self.data = data
        self._update_size()

    def get_superres(self, upscale: int = 4, new_name: str = None) -> TArtefact:
        """
        Return a version of the current artefact in an AI-upsampled resolution
        :param upscale:
        :return:
        """
        if upscale not in (2, 3, 4):
            raise ValueError("Upscale should be 2, 3, or 4")
        superres = self.get_superres_ml_model(upscale)
        return Artefact(
            name=new_name or self._insert_suffix(self.name, suffix=f"@x{upscale}"),
            data=superres.upsample(self.data),
        )

    @staticmethod
    def _insert_suffix(file_name: str, suffix=None) -> str:
        path = Path(file_name)
        if suffix:
            file_name = path.stem + suffix + path.suffix
        return file_name

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

    def get_superres_pil(self, pil_image: Image, upscale: int = 4) -> Image:
        cv2_img: np.ndarray = self.pil_to_cv2(img=pil_image)
        cv_superres = self.get_superres(cv2_img, upscale)
        return self.cv2_to_pil(cv_superres)

    @staticmethod
    def cv2_to_pil(data: np.ndarray) -> Image:
        return Image.fromarray(cv2.cvtColor(data, cv2.COLOR_BGR2RGB))

    @staticmethod
    def pil_to_cv2(img: Image) -> np.ndarray:
        pil_as_arr = np.array(img)
        return cv2.cvtColor(pil_as_arr, cv2.COLOR_RGB2BGR)

    def save(self, project: Project, suffix: Optional[str] = None) -> None:
        """
        Save this artefact into a project
        :param project: a Project instance
        :param suffix: suffix to insert into the file name. For example,
                        if the suffix is @3x and the artefact name is icon.png,
                        then the filename becomes icon@3x.png.
        :return:
        """
        file_name = self._insert_suffix(self.name, suffix)
        project.save_png(data=self.data, file_name=Path(file_name))

    def fill(self, rgb: Tuple) -> None:
        image: Image = Image.new("RGB", self.size)
        image.paste(rgb, [0, 0, self.width, self.height])
        self.data = np.array(image)
