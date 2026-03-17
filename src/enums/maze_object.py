from enum import Enum


class MazeObject(Enum):
    WALL = "Walls"
    PATH = "Path"
    ENTRY = "Entry"
    EXIT = "Exit"
    FT = "42"
