from abc import ABC
from pathlib import Path

from project_util.naming.naming import NamingUtil
from project_util.project.project import Project


class Blueprint(ABC):
    def export(self) -> str:
        """
        This should return a string representing the blueprint in a way that could be
        neatly printed to the command line or saved as a (text) file.
        :return: human-readable JSON/YAML/Dict/.. of the blueprint
        """
        raise NotImplementedError


class BlueprintProcessor(ABC):
    def __init__(
        self, name, module=None, parent_level=0, suffix_fn=NamingUtil.format_now
    ):
        parent_dir = Path(module).parents[parent_level] if module else Path()

        name = f"{name}-{suffix_fn()}" if suffix_fn else name

        self.project = Project(
            name=name,
            parent_dir=parent_dir,
        )

    def process(self, blueprint: Blueprint):
        raise NotImplementedError
