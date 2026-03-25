from typing import Iterable
from .window import Window
from ..position import Position as Vec2
from ..utils import colorize, bold
from ..enums import Color


class WindowManager:
    def __init__(self) -> None:
        self.title: Window = Window("PROJECT BY LLOBET AND QCORSIUS",
                                      Vec2(x=1, y=1), Vec2(x=88, y=9))
        self.main: Window = Window("MAIN MENU", Vec2(x=1, y=10),
                                     Vec2(x=35, y=8))
        self.options: Window = Window("OPTIONS", Vec2(x=1, y=10),
                                        Vec2(x=35, y=8))
        self.__active: Window = self.main

    def display_title(self) -> None:
        with open("src/assets/title.txt") as f:
            self.title.draw_frame()
            self.title.clear()
            self.title.write(colorize(f.read(), Color.BLUE), Vec2(x=3, y=2))

    def display_main_menu(self) -> None:
        self.main.draw_frame()
        self.main.clear()
        self.main.write(bold(colorize(">>> GENERATE MAZE", Color.PURPLE)),
                          Vec2(x=2, y=1))
        self.main.write(colorize("SOLVE MAZE", Color.WHITE), Vec2(x=2, y=2))
        self.main.write(colorize("ERASE MAZE", Color.WHITE), Vec2(x=2, y=3))
        self.main.write(colorize("OPTIONS", Color.WHITE), Vec2(x=2, y=4))
        self.main.write(colorize("CONTRIBUTIONS", Color.WHITE),
                          Vec2(x=2, y=5))
        self.main.write(colorize("EXIT", Color.RED), Vec2(x=2, y=6))

    def display_options(self) -> None:
        self.options.draw_frame()
        self.options.clear()
        self.options.write(bold(colorize(">>> MAZE CONFIG", Color.PURPLE)),
                                  Vec2(x=2, y=1))
        self.options.write(colorize("COLOR OPTIONS", Color.WHITE),
                             Vec2(x=2, y=2))
        self.options.write(colorize("ANIMATION OPTIONS", Color.WHITE),
                             Vec2(x=2, y=3))
        self.options.write(colorize("GO BACK", Color.RED),
                             Vec2(x=2, y=4))

    def set_active(self, menu: Window) -> None:
        self.__active = menu

    def get_active(self) -> Window:
        return self.__active