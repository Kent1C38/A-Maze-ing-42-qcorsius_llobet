from ..config import Configuration
from ..position import Position
from ..enums import Color, MazeObject
from ..utils import (
    colorize,
    move_down,
    move_up,
    move_left,
    move_right,
    move_to
)
from sys import stdout
from time import sleep
from typing import Tuple


class Map:
    """
    Visualizer map class.

    This class takes care of all the display process. It displays the maze,
    the path, entry and exit points as well as the 42 logo along all their
    respective colors. All this logic is in a separate class to avoid having
    a single class with too much responsibility, otherwise known as a
    God Object.
    """
    def __init__(self, config: Configuration) -> None:
        """
        Initializes and returns a new visualizer map.

        This is the main object that takes care of the maze display on the
        terminal. It contains several methods used to edit and show the maze
        on screen. It has its own map and does not use the maze object due to
        it being encapsulated within this very object.

        Args:
            config (Configuration): The config used to initialize properties.

        Returns:
            none (None):
        """
        self.__config: Configuration = config
        self.__map = [[" " for _ in range(self.__config.width * 4 + 2)]
                      for _ in range(self.__config.height * 2 + 1)]
        self.__wall_color: Color = Color.WHITE
        self.__path_color: Color = Color.BLUE
        self.__entry_color: Color = Color.GREEN
        self.__exit_color: Color = Color.RED
        self.__path: str = ""
        self.__42_color: Color = Color.CYAN

    def add_cell(self, x: int, y: int, cell: str) -> None:
        """
        Adds a single cell to the visualizer.

        This is useful when you need to only add one cell at a specific
        location. It is used for example by the add_ft method to place down
        the correct cells.

        Args:
            x (int): The X coordinate of the cell.
            y (int): The Y coordinate of the cell.
            cell (str): The character to display for this cell.

        Returns:
            none (None):
        """
        self.__map[y * 2 + 1][x * 4 + 1] = cell
        self.__map[y * 2 + 1][x * 4 + 2] = cell

    def add_walls(self, walls: str) -> None:
        """
        Adds the maze walls to the visualizer.

        Takes a hexadecimal representation of the maze and adds all its cells
        to the visualizer map.

        Args:
            walls (str): A hexadecimal representation of the walls.

        Returns:
            none (None):
        """
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
            j += 4

    def add_path(self, x: int, y: int, path: str) -> None:
        """
        Adds the path from the entry to the exit to the visualizer.

        Takes the coordinates of the entry point and adds the path cells
        relative to this entry.

        Args:
            x (int): The X coordinate of the entry point.
            y (int): The Y coordinate of the entry point.
            path (str): The path from the entry to the exit.

        Returns:
            none (None):
        """
        path_char: str = colorize("█", self.__path_color)

        self.__path = path
        x *= 4
        y *= 2
        for index, char in enumerate(path):
            if not index == 0:
                self.__map[y + 1][x + 1] = path_char
                self.__map[y + 1][x + 2] = path_char
            match char:
                case "N":
                    self.__map[y][x + 1] = path_char
                    self.__map[y][x + 2] = path_char
                    y -= 2
                case "E":
                    self.__map[y + 1][x + 3] = path_char
                    self.__map[y + 1][x + 4] = path_char
                    x += 4
                case "S":
                    self.__map[y + 2][x + 1] = path_char
                    self.__map[y + 2][x + 2] = path_char
                    y += 2
                case "W":
                    self.__map[y + 1][x - 1] = path_char
                    self.__map[y + 1][x] = path_char
                    x -= 4

    def add_entry(self, pos: Position) -> None:
        """
        Adds the entry point to the visualizer.

        Takes its coordinates and adds it to the visualizer map.

        Args:
            pos (Position): The coordinates of the entry point.

        Returns:
            none (None):
        """
        entry_char: str = colorize("█", self.__entry_color)

        self.add_cell(pos.x, pos.y, entry_char)

    def add_exit(self, pos: Position) -> None:
        """
        Adds the exit point to the visualizer.

        Takes its coordinates and adds it to the visualizer map.

        Args:
            pos (Position): The coordinates of the exit point.

        Returns:
            none (None):
        """
        exit_char: str = colorize("█", self.__exit_color)

        self.add_cell(pos.x, pos.y, exit_char)

    def add_ft(self, x: int, y: int) -> None:
        """
        Adds the 42 logo to the visualizer.

        Takes the X and Y coordinates of the top left corner of the logo and
        adds it to the visualizer map relative to this position.

        Args:
            x (int): The X coordinate of the top left corner.
            y (int): The Y coordinate of the top left corner.

        Returns:
            none (None):
        """
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

    def visualize(self) -> None:
        """
        Displays the generated maze on screen.

        This is the main function to display it on the terminal. Does not
        account for animations whatsoever.

        Args:
            none (None):

        Returns:
            none (None):
        """
        string: str = ""

        move_to(0, 0)
        for row in self.__map:
            for char in row:
                string += char
            string += "\n"
        print(string)

    def reset(self) -> None:
        """
        Resets the visualizer.

        Used to clear the display for generating a new maze.

        Args:
            none (None):

        Returns:
            none (None):
        """
        self.__map = [[" " for _ in range(self.__config.width * 4 + 2)]
                      for _ in range(self.__config.height * 2 + 1)]

    def change_color(self, obj: MazeObject, color: Color) -> None:
        """
        Changes the color of one part of the maze.

        Checks the specified maze object to change and sets the passed color
        as its new color.

        Args:
            obj (MazeObject): An enum representing one part of the maze.
            color (Color): An enum representing a color.

        Returns:
            none (None):
        """
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

    def animate_maze(self, wall: int, x: int, y: int, w: int, h: int) -> None:
        """
        Animates the maze generation on screen.

        A newly generated maze with all its walls must be displayed first. Then
        it will carve down this maze, deleting characters making the walls on
        display until the maze is displayed correctly.

        Args:
            wall (int): The walls to carve out.
            x (int): The X coordinate of the cell.
            y (int): The Y coordinate of the cell.
            w (int): The width of the maze
            h (int): The height of the maze.

        Returns:
            none (None):
        """
        move_up(h * 2)
        move_left(w * 4)
        move_down(y * 2 + 1)
        move_right(x * 4 + 1)

        stdout.flush()
        if not wall & 0x1:
            move_up(1)
            stdout.write("\033[96m  \033[0")
            move_left(2)
            move_down(1)
        if not wall & 0x2:
            move_right(2)
            stdout.write("\033[96m  \033[0")
            move_left(4)
        if not wall & 0x4:
            move_down(1)
            stdout.write("\033[96m  \033[0")
            move_left(2)
            move_up(1)
        if not wall & 0x8:
            move_left(2)
            stdout.write("\033[96m  \033[0")
        move_up(h * 2)
        move_down((h - y) * 2 - 1)
        move_left(w * 4)
        move_right((w - x) * 4 - 2)
        sleep(0.01)

    def animate_path(self) -> None:
        """
        Animates the path solver on screen.

        Moves the cursor to the entry point and starts displaying the path.
        It will progressively appear until it reaches the exit point.

        Args:
            none (None):

        Returns:
            none (None):
        """
        x: int = self.__config.entry_pos.x
        y: int = self.__config.entry_pos.y

        move_to(x * 4 + 2, y * 2 + 2)
        for c in self.__path:
            stdout.flush()
            stdout.write(colorize("██", self.__path_color))
            move_left(2)
            if c == "N":
                y -= 1
                move_up(1)
                stdout.write(colorize("██", self.__path_color))
                move_up(1)
                move_left(2)
            elif c == "E":
                x += 1
                move_right(2)
                stdout.write(colorize("██", self.__path_color))
            elif c == "S":
                y += 1
                move_down(1)
                stdout.write(colorize("██", self.__path_color))
                move_down(1)
                move_left(2)
            elif c == "W":
                x -= 1
                move_left(2)
                stdout.write(colorize("██", self.__path_color))
                move_left(4)
            sleep(0.01)

    def get_colors(self) -> Tuple[Color, Color, Color, Color, Color]:
        """
        Returns the colors of the maze.

        Used for UI.

        Args:
            none (None):

        Returns:
            colors (Tuple): Colors
        """
        return (self.__wall_color,
                self.__path_color,
                self.__entry_color,
                self.__exit_color,
                self.__42_color)
