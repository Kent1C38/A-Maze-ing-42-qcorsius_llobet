from ..config import Configuration, ConfigValues
from ..position import Position
from ..enums import Color, MazeObject
from ..utils import colorize


class Map:
    def __init__(self: "Map", config: Configuration) -> None:
        self.__width = config.width
        self.__height = config.height
        self.__map = [[" " for _ in range(self.__width * 3 + 2)]
                      for _ in range(self.__height * 2 + 1)]
        self.__wall_color: Color = Color.WHITE
        self.__path_color: Color = Color.WHITE
        self.__entry_color: Color = Color.GREEN
        self.__exit_color: Color = Color.RED
        self.__42_color: Color = Color.CYAN

    def get_width(self: "Map") -> int:
        return self.__width

    def get_height(self: "Map") -> int:
        return self.__height

    def add_cell(self: "Map", x: int, y: int, cell: str) -> None:
        self.__map[y * 2 + 1][x * 3 + 1] = cell
        self.__map[y * 2 + 1][x * 3 + 2] = cell

    def add_walls(self: "Map", walls: str) -> None:
        i: int = 0
        j: int = 0
        block: str = colorize("█", self.__wall_color)

        for char in walls:
            if char == "\n":
                j = 0
                i += 2
                continue
            n: int = int(char, base=16)

            self.__map[i][j] = block
            self.__map[i][j + 3] = block
            self.__map[i + 2][j] = block
            self.__map[i + 2][j + 3] = block
            if n & 0x1:
                self.__map[i][j + 1] = block
                self.__map[i][j + 2] = block
            if n & 0x2:
                self.__map[i + 1][j + 3] = block
            if n & 0x4:
                self.__map[i + 2][j + 1] = block
                self.__map[i + 2][j + 2] = block
            if n & 0x8:
                self.__map[i + 1][j] = block
            j += 3

    def add_path(self: "Map", x: int, y: int, path: str) -> None:
        x: int = x * 3
        y: int = y * 2
        path_char: str = colorize("█", self.__path_color)

        for char in path:
            self.__map[y + 1][x + 1] = path_char
            self.__map[y + 1][x + 2] = path_char
            match char:
                case "N":
                    self.__map[y][x + 1] = path_char
                    self.__map[y][x + 2] = path_char
                    y -= 2
                case "E":
                    self.__map[y + 1][x + 3] = path_char
                    x += 3
                case "S":
                    self.__map[y + 2][x + 1] = path_char
                    self.__map[y + 2][x + 2] = path_char
                    y += 2
                case "W":
                    self.__map[y + 1][x] = path_char
                    x -= 3

    def add_entry(self: "Map", pos: Position) -> None:
        entry_char: str = colorize("█", self.__entry_color)

        self.add_cell(pos.x, pos.y, entry_char)

    def add_exit(self: "Map", pos: Position) -> None:
        exit_char: str = colorize("█", self.__exit_color)

        self.add_cell(pos.x, pos.y, exit_char)

    def add_ft(self: "Map", x: int, y: int) -> None:
        ft_char: str = colorize("█", self.__42_color)

        self.add_cell(x, y, ft_char)
        self.add_cell(x, y + 1, ft_char)
        self.add_cell(x, y + 2, ft_char)
        self.add_cell(x + 1, y + 2, ft_char)
        self.add_cell(x + 2, y + 2, ft_char)
        self.add_cell(x + 2, y + 3, ft_char)
        self.add_cell(x + 2, y + 4, ft_char)
        self.add_cell(x + 4, y, ft_char)
        self.add_cell(x + 5, y, ft_char)
        self.add_cell(x + 6, y, ft_char)
        self.add_cell(x + 6, y + 1, ft_char)
        self.add_cell(x + 6, y + 2, ft_char)
        self.add_cell(x + 5, y + 2, ft_char)
        self.add_cell(x + 4, y + 2, ft_char)
        self.add_cell(x + 4, y + 3, ft_char)
        self.add_cell(x + 4, y + 4, ft_char)
        self.add_cell(x + 5, y + 4, ft_char)
        self.add_cell(x + 6, y + 4, ft_char)

    def visualize(self: "Map") -> None:
        string: map = ""

        for row in self.__map:
            for char in row:
                string += char
            string += "\n"
        print(string)

    def reset(self) -> None:
        self.__map = [[" " for _ in range(self.__width * 3 + 2)]
                      for _ in range(self.__height * 2 + 1)]

    def change_color(self, obj: MazeObject, color: Color) -> None:
        match obj.value:
            case "Walls":
                self.__wall_color = color
            case "Path":
                self.__path_color = color
            case "Entry":
                self.__entry_color = color
            case "Exit":
                self.__exit_color = color
            case "42":
                self.__42_color = color
