import datetime
from pathlib import Path
from os import listdir, makedirs
from os.path import isfile, join
from random import randint

from constants import GREEK_ALPHABET


class Project:
    def __init__(self, name: str, parent_dir: Path):
        self._parent_dir = parent_dir
        self._name = name
        self._project_dir: Path = self._make_project_dir(self._name)
        self._folders = []

    def _make_project_dir(self, name: str) -> Path:
        path = Path(join(self._parent_dir, name))
        makedirs(path, exist_ok=True)
        return path

    @property
    def path(self) -> Path:
        return self._project_dir

    @staticmethod
    def now() -> datetime:
        return datetime.datetime.now().replace(microsecond=0)

    @staticmethod
    def format_iso(date):
        return date.isoformat().replace(":", "")

    @staticmethod
    def get_file_names(path: Path):
        return [f for f in listdir(path) if isfile(join(path, f))]

    def save_png(self, file_name):
        pass

    def add_folder(self, name: str):
        if getattr(self, name, None):
            raise ValueError("Name not available")
        sub_folder = Project(name, parent_dir=self._project_dir)
        self._folders.append(sub_folder)
        setattr(self, name, sub_folder)

    @staticmethod
    def random_name() -> str:
        return GREEK_ALPHABET[randint(0, len(GREEK_ALPHABET))]
