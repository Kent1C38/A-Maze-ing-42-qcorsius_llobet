from enum import Enum


class Facing(Enum):
    """
    The Facing enum.

    This has been created to represent walls more easily, instead of just
    hardcoding all the values in our code.
    """
    NORTH = (0b0001, (0, -1))
    EAST = (0b0010, (1, 0))
    SOUTH = (0b0100, (0, 1))
    WEST = (0b1000, (-1, 0))

    @property
    def bin_value(self) -> int:
        """
        Returns the value of the wall.

        1 means North.
        2 means East.
        4 means South.
        8 means West.

        This should be used if getting the value of the wall is necessary. Do
        not do Face.value[0] as it would be confusing.

        Args:
            none (None):

        Returns:
            value (int): The value of the wall.
        """
        return self.value[0]

    @property
    def dx(self) -> int:
        """
        Returns the X coordinate of the face.

        Used to check for walls.

        Args:
            none (None):

        Returns:
            value (int): The X coordinate.
        """
        return self.value[1][0]

    @property
    def dy(self) -> int:
        """
        Returns the Y coordinate of the face.

        Used to check for walls.

        Args:
            none (None):

        Returns:
            value (int): The Y coordinate.
        """
        return self.value[1][1]

    @property
    def vector(self) -> tuple[int, int]:
        """
        Returns the coordinates of the face.

        Used to check for walls.

        Args:
            none (None):

        Returns:
            vec (tuple[int, int]): The coordinates.
        """
        return self.value[1]


class Cell:
    """
    The Cell class.

    This class is used to represent indivudual cells in the maze. It contains
    logic and methods related to wall state and placement. Used to define the
    behavior of walls.
    """
    def __init__(self) -> None:
        """
        Returns a new Cell.

        Creates a new cell with all walls set.

        Args:
            none (None):

        Returns:
            none (None):
        """
        self.__walls = 0b1111
        self.is_visited = False
        self.is_unbreakable = False

    def set_unbreakable(self, is_unbreakable: bool) -> None:
        """
        Sets the unbreakable property of the cell.

        This property determines if the maze algorithm can delete its walls
        or not. This is used to make the walls forming the 42 logo immute to
        modification, preserving the logo and its state.

        Args:
            is_unbreakable (bool): The state of the property.

        Returns:
            none (None):
        """
        self.is_unbreakable = is_unbreakable

    def wall_request(self, face: Facing) -> bool:
        return bool(self.__walls & face.bin_value)

    def break_wall(self, facing: Facing) -> None:
        self.__walls -= facing.bin_value

    def get_active_walls(self) -> int:
        return self.__walls

    def reset(self) -> None:
        self.__walls = 0b1111
        self.is_visited = False
        self.is_unbreakable = False
