from enum import Enum


class Limits(Enum):
    """
    The Limits enum.

    Represents the size limitations of a maze configuration.
    """
    MIN_WIDTH = 11
    MAX_WIDTH = 100
    MIN_HEIGHT = 9
    MAX_HEIGHT = 100
