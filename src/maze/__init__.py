from ..utils import is_pos_valid, get_42logo_cells
from ..config import Configuration
from .cell import Cell, Facing
from .visualizer import Map
from random import Random
from ..enums import Color, MazeObject
from ..position import Position
from sys import stdout, setrecursionlimit, maxsize
from os import system

setrecursionlimit(10000)


class Maze:
    def __init__(self, config: Configuration):
        self.__maze = [[Cell()
                        for _ in range(config.width)]
                       for _ in range(config.height)]
        self.__config = config
        self.__bounds = (self.__config.width,
                         self.__config.height)
        self.__visualizer = Map(config)

        self.__visualizer.add_entry(config.entry_pos)
        self.__visualizer.add_exit(config.exit_pos)
        self.__generate: bool = False
        self.__anim_maze: bool = False
        self.__anim_path: bool = False

    def get(self) -> list[list[Cell]]:
        return self.__maze

    def convert_to_hex_str(self) -> str:
        string = ""
        lab: list[list[Cell]] = self.__maze
        for line in lab:
            for cell in line:
                string += f"{cell.get_active_walls():x}".upper() \
                    if cell else "0"
            string += "\n"
        return string

    def gen_ft_logo(self) -> None:
        x_center = self.__config.width // 2
        y_center = self.__config.height // 2
        start = Position(x=x_center - 3, y=y_center - 2)

        logo_cells = get_42logo_cells(
            self.__config.width, self.__config.height)

        for p in logo_cells:
            self.get()[p[1]][p[0]].set_unbreakable(True)

        self.__visualizer.add_ft(start.x, start.y)

    def would_excede_room_limit(self, x: int, y: int, facing: Facing) -> bool:
        grid = self.get()
        target_x = x + facing.dx
        target_y = y + facing.dy

        def opposite(f: Facing) -> Facing:
            return {
                Facing.NORTH: Facing.SOUTH,
                Facing.SOUTH: Facing.NORTH,
                Facing.WEST: Facing.EAST,
                Facing.EAST: Facing.WEST
            }[f]

        visited = set()
        stack = [(target_x, target_y)]

        min_x = max_x = target_x
        min_y = max_y = target_y

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))

            min_x = min(min_x, cx)
            max_x = max(max_x, cx)
            min_y = min(min_y, cy)
            max_y = max(max_y, cy)

            cell = grid[cy][cx]
            open_walls = 4 - cell.get_active_walls().bit_count()
            if open_walls < 2:
                continue

            if len(visited) > 6:
                return True

            for f in Facing:
                nx, ny = cx + f.dx, cy + f.dy
                if not is_pos_valid(nx, ny, self.__bounds):
                    continue

                wall_between = (cx == x and cy == y and f == facing) or \
                    (cx == target_x and cy ==
                     target_y and f == opposite(facing))

                if not cell.wall_request(f) or wall_between:
                    if (nx, ny) not in visited:
                        stack.append((nx, ny))

        width = max_x - min_x + 1
        height = max_y - min_y + 1
        if width > 3 or height > 3:
            return True

        return False

    def generate(self, keep_seed: bool = False) -> bool:
        self.reset()
        if not keep_seed:
            self.new_rand_seed()
        rng = Random(self.__config.seed)

        self.gen_ft_logo()

        start: Position = self.__config.entry_pos

        system("clear")
        self.__visualizer.reset()
        self.__visualizer.add_walls(self.convert_to_hex_str())
        self.visualize()
        self.crawl(start.x, start.y, rng)

        if not self.__config.perfect:
            chance = 70.0
            x, y = 0, 0
            for y in range(self.__config.height):
                for x in range(self.__config.width):
                    if rng.randint(0, 100) < chance:
                        cell = self.get()[y][x]

                        if cell.is_unbreakable:
                            continue

                        walls = [f for f in Facing if cell.wall_request(f)]

                        if len(walls) == 0:
                            continue

                        di: Facing = rng.choice(walls)

                        if not is_pos_valid(x + di.dx, y + di.dy,
                                            self.__bounds):
                            continue

                        if self.get()[y + di.dy][x + di.dx].is_unbreakable:
                            continue

                        if self.would_excede_room_limit(x, y, di):
                            continue

                        self.get()[y][x].break_wall(di)
                        self.get()[y + di.dy][x + di.dx].break_wall({
                            Facing.NORTH: Facing.SOUTH,
                            Facing.SOUTH: Facing.NORTH,
                            Facing.EAST: Facing.WEST,
                            Facing.WEST: Facing.EAST
                        }[di])

        self.__visualizer.reset()
        self.__visualizer.add_entry(self.__config.entry_pos)
        self.__visualizer.add_exit(self.__config.exit_pos)
        self.__visualizer.add_walls(self.convert_to_hex_str())
        self.__generate = True
        self.gen_ft_logo()
        stdout.flush()

    def crawl(self, x: int, y: int, rng: Random) -> bool:
        self.get()[y][x].is_visited = True
        directions = [f for f in Facing if self.get()[y][x].wall_request(f)]
        while directions:
            f = directions.pop(rng.randint(0, len(directions) - 1))
            nx, ny = x + f.dx, y + f.dy

            if not is_pos_valid(nx, ny, self.__bounds):
                continue

            if self.get()[ny][nx].is_visited:
                continue

            if self.get()[ny][nx].is_unbreakable:
                continue

            if self.would_excede_room_limit(x, y, f):
                continue

            self.get()[y][x].break_wall(f)
            self.get()[ny][nx].break_wall({
                Facing.NORTH: Facing.SOUTH,
                Facing.SOUTH: Facing.NORTH,
                Facing.WEST: Facing.EAST,
                Facing.EAST: Facing.WEST
            }[f])

            if self.__anim_maze:
                self.__visualizer.crawl(self.get()[y][x].get_active_walls(),
                                        x, y, self.__config.width,
                                        self.__config.height)
            self.crawl(nx, ny, rng)
        return True

    def new_rand_seed(self) -> None:
        rand = Random(self.__config.seed)
        self.__config.replace_seed(rand.randint(-maxsize - 1, maxsize))

    def reset_visited(self) -> None:
        for line in self.get():
            for cell in line:
                cell.is_visited = True

    def reset(self) -> None:
        for line in self.get():
            for cell in line:
                cell.reset()
        self.__visualizer.reset()

    def visualize(self) -> None:
        self.__visualizer.visualize()

    def set_color(self, obj: MazeObject, color: Color) -> None:
        self.__visualizer.change_color(obj, color)
        if self.__generate:
            self.generate(True)

    def switch_animation_state(self, obj: MazeObject) -> None:
        match obj.value:
            case "Walls":
                self.__anim_maze = not self.__anim_maze
            case "Path":
                self.__anim_path = not self.__anim_path

    def get_animation_state(self, obj: MazeObject) -> bool:
        match obj.value:
            case "Walls":
                return self.__anim_maze
            case "Path":
                return self.__anim_path
            case _:
                return None

    def get_status(self) -> bool:
        return self.__generate

    def hide(self) -> None:
        self.__generate = False
