from abc import ABC


class Blueprint(ABC):
    pass

    def export(self) -> str:
        """
        This should return a string representing the blueprint in a way that could be
        neatly printed to the command line or saved as a (text) file.
        :return:
        """
        raise NotImplementedError


class BlueprintProcessor(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def process(self, blueprint: Blueprint):
        raise NotImplementedError
