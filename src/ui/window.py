from ..position import Position as Vec2
from ..utils import move_cursor
from ..enums import Color
from sys import stdout
from typing import List

class Window:
    def __init__(self, title: str, pos: Vec2, size: Vec2) -> None:
        self.__title: str = title
        self.__position: Vec2 = pos
        self.__size: Vec2 = size
        self.__color: Color = Color.WHITE
        self.__written: List[str] = []
        self.__cursor: int = 0

    def draw_frame(self) -> None:
        x: int = self.__position.x
        y: int = self.__position.y
        w: int = self.__size.x
        h: int = self.__size.y
        t: str = f"═╣ {self.__title} ╠═"

        move_cursor(Vec2(x=x, y=y))
        stdout.write(f"\033[{self.__color.value}m╔")
        if len(t) < w:
            stdout.write(t)
        stdout.write("═" * (w - (len(t) + 2)))
        stdout.write("╗\n")
        for i in range(h - 2):
            move_cursor(Vec2(x=x, y=y + i + 1))
            stdout.write("║")
            move_cursor(Vec2(x=x + w - 1, y=y + i + 1))
            stdout.write("║\n")
        move_cursor(Vec2(x=x, y=y + h - 1))
        stdout.write("╚")
        stdout.write("═" * (w - 2))
        stdout.write("╝\033[0m")
        stdout.flush()

    def clear(self) -> None:
        x: int = self.__position.x
        y: int = self.__position.y
        w: int = self.__size.x
        h: int = self.__size.y

        for i in range(self.__size.y - 2):
            move_cursor(Vec2(x=x + 1, y=y + i + 1))
            stdout.write(" " * (w - 2))
        move_cursor(Vec2(x=x + w, y=y + h - 1))

    def write(self, txt: str, pos: Vec2, idx: int | None = None) -> None:
        x: int = self.__position.x
        y: int = self.__position.y
        w: int = self.__size.x
        h: int = self.__size.y
        i: int = 0
        j: int = 0

        if idx:
            self.__written.insert(idx, txt)
        else:
            self.__written.append(txt)
        for line in txt.splitlines():
            if pos.y + i < 1 or pos.y + i > h - 2:
                i += 1
                continue
            move_cursor(Vec2(x=x + pos.x, y=y + pos.y + i))
            j = 0
            for c in line:
                if pos.x + j < 1 or pos.x + j > w - 2:
                    j += 1
                    move_cursor(Vec2(x=x + pos.x + j, y=y + pos.y + i))
                    continue
                stdout.write(c)
                j += 1
            i += 1
        move_cursor(Vec2(x=x, y=y + h))
        stdout.flush()

    def read(self, idx: int | None = None) -> str:
        if idx:
            return self.__written[idx]
        else:
            return self.__written[self.__cursor]

    def move_up(self) -> int:
        self.__cursor = (self.__cursor - 1) % max(len(self.__written), 1)
        return self.__cursor

    def move_down(self) -> int:
        self.__cursor = (self.__cursor + 1) % max(len(self.__written), 1)
        return self.__cursor

    def set_color(self, color: Color) -> None:
        self.__color = color