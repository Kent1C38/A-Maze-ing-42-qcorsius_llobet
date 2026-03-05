from ..config import Configuration, ConfigValues
from .cell import Cell


class Labyrinth:
    def __init__(self, config: Configuration):
        self.__labyrinth = [[None for _
                             in range(0, config.get(ConfigValues.HEIGHT))]
                            for _ in range(config.get(ConfigValues.WIDTH))]
        self.__config = config

    def get(self) -> list[list[Cell]]:
        return self.__labyrinth
