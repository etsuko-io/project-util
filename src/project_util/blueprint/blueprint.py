from abc import ABC


class Blueprint(ABC):
    def export(self) -> str:
        """
        This should return a string representing the blueprint in a way that could be
        neatly printed to the command line or saved as a (text) file.
        :return: human-readable JSON/YAML/Dict/.. of the blueprint
        """
        raise NotImplementedError
