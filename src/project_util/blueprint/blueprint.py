from abc import ABC


class Blueprint(ABC):
    pass


class BlueprintProcessor(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def process(self, blueprint: Blueprint):
        raise NotImplementedError
