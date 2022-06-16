import datetime
from pathlib import Path
from os import listdir, makedirs
from os.path import isfile, join


class Project:
    def __init__(self, name: str, parent_dir: Path):
        self._parent_dir = parent_dir
        self._name = name
        self._make_project_dir(self._name)

    def _make_project_dir(self, name: str):
        makedirs(join(self._parent_dir, name), exist_ok=True)

    @staticmethod
    def now() -> datetime:
        return datetime.datetime.now().replace(microsecond=0)

    @staticmethod
    def format_iso(date):
        return date.isoformat().replace(":", "")

    @staticmethod
    def get_file_names(path: Path):
        return [f for f in listdir(path) if isfile(join(path, f))]
