class Position:
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y

    @staticmethod
    def from_str(string: str) -> "Position":
        splited = string.split(',')
        if not len(splited) == 2:
            raise Exception(f"Invalid position: {string}")
        else:
            x = int(splited[0])
            y = int(splited[1])
            return Position(x, y)

    def __str__(self):
        return f"(x={self.get_x()}, y={self.get_y()})"
