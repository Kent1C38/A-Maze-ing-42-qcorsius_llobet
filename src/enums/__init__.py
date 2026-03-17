from .color import Color
from .maze_object import MazeObject


if __name__ == "__main__":
    for c in Color:
        print(c.value)
    for obj in MazeObject:
        print(obj.value)
