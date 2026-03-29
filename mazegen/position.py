from pydantic import BaseModel, Field


class Position(BaseModel):
    """
    Class to create points in a 2D space.

    Instances are created by calling Position() and passing parameters as
    kwargs. It then returns a Position object. We use Pydantic for automatic
    type validation.

    Args:
        x (int): The X coordinate.
        y (int): The Y coordinate.

    Returns:
        position (Position): The 2D position.

    Raises:
        ValidationError:
    """
    x: int = Field(strict=True)
    y: int = Field(strict=True)

    @staticmethod
    def from_str(string: str) -> "Position":
        """
        Returns a new Position from a string.

        Takes a string, splits it at the first occurence of a comma, then
        returns a new Position.

        Args:
            string (str): The position as string.

        Returns:
            position (Position): The newly created position.
        """
        try:
            x, y = string.split(',', 1)
            x = x.strip()
            y = y.strip()

            return Position(x=int(x), y=int(y))
        except Exception as e:
            raise Exception(f"Failed to create position from string {string}: "
                            f"{e}")

    def heuristic(self, destination: "Position") -> int:
        """
        Calculates the distance between two Positions.

        Substracts the destination's position by its own position and returns
        the absolute value.

        Args:
            destination (Position): The second point.

        Returns:
            distance (int): The calculated distance between the two points.
        """
        return abs(destination.x - self.x) + abs(destination.y - self.y)

    def get(self) -> tuple[int, int]:
        """
        Returns the coordinates of the Position as a tuple.

        Args:
            none (None):

        Returns:
            coordinates (tuple[int, int]): The coordinates of the Position.
        """
        return (self.x, self.y)

    def __str__(self) -> str:
        """
        To format printing.

        Args:
            none (None):

        Returns:
            str (str): The formatted string.
        """
        return f"(x={self.x}, y={self.y})"
