from pydantic import BaseModel, Field


class Position(BaseModel):
    x: int = Field(strict=True)
    y: int = Field(strict=True)

    @staticmethod
    def from_str(string: str) -> "Position":
        try:
            x, y = string.split(',', 1)
            x = x.strip()
            y = y.strip()

            return Position(x=int(x), y=int(y))
        except Exception as e:
            raise Exception(f"Failed to create position from string {string}: "
                            f"{e}")

    def heuristic(self, destination: "Position"):
        return abs(destination.x - self.x) + abs(destination.y - self.y)

    def get(self) -> tuple[int, int]:
        return (self.x, self.y)

    def __str__(self):
        return f"(x={self.get_x()}, y={self.get_y()})"
