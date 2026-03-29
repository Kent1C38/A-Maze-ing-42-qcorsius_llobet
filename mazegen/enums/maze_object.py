from enum import Enum


class MazeObject(Enum):
    """
    The MazeObject enum.

    Represents all object types in a maze.
    """
    WALL = "Walls"
    PATH = "Path"
    ENTRY = "Entry"
    EXIT = "Exit"
    FT = "42"
