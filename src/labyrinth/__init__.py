from ..utils import is_pos_valid
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

    def set_cell(self, x: int, y: int, cell: Cell):
        if is_pos_valid(x, y, (self.__config.get(ConfigValues.WIDTH),
                               self.__config.get(ConfigValues.HEIGHT))):
            self.__labyrinth[x][y] = cell
        else:
            raise Exception(
                f"Could not set cell data in position (x={x},y={y}): " +
                "Invalid position!")

    def convert_to_hex_str(self) -> str:
        string = ""
        lab: list[list[Cell]] = self.__labyrinth
        for line in lab:
            for cell in line:
                if cell:
                    string += f"{cell.get_active_walls():x}".upper()
                else:
                    string += "0"
            string += "\n"
        return string
