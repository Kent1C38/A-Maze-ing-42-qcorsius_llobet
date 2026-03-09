from ..utils import is_pos_valid
from ..config import Configuration, ConfigValues
from .cell import Cell, Facing
from random import Random


class Labyrinth:
    def __init__(self, config: Configuration):
        self.__maze = [[Cell(True, True, True, True) for _
                        in range(0, config.get(ConfigValues.HEIGHT))]
                       for _ in range(config.get(ConfigValues.WIDTH))]
        self.__config = config
        self.__bounds = (self.__config.get(ConfigValues.WIDTH),
                         self.__config.get(ConfigValues.HEIGHT))

    def get(self) -> list[list[Cell]]:
        return self.__maze

    def set_cell(self, x: int, y: int, cell: Cell):
        if is_pos_valid(x, y, self.__bounds):
            self.__maze[x][y] = cell
        else:
            raise Exception(
                f"Could not set cell data in position (x={x},y={y}): " +
                "Invalid position!")

    def convert_to_hex_str(self) -> str:
        string = ""
        lab: list[list[Cell]] = self.__maze
        for line in lab:
            for cell in line:
                if cell:
                    string += f"{cell.get_active_walls():x}".upper()
                else:
                    string += "0"
            string += "\n"
        return string

    def would_excede_room_limit(self, x: int, y: int, facing: Facing):
        grid = self.get()

        target_x = x + (facing == Facing.EAST) - (facing == Facing.WEST)
        target_y = y + (facing == Facing.SOUTH) - (facing == Facing.NORTH)

        nx, ny = x, y
        match facing:
            case Facing.NORTH: ny += 1
            case Facing.WEST: nx += 1
            case Facing.SOUTH: ny -= 1
            case Facing.EAST: nx -= 1

        def opposite(f: Facing) -> Facing:
            return {
                Facing.NORTH: Facing.SOUTH,
                Facing.SOUTH: Facing.NORTH,
                Facing.WEST: Facing.EAST,
                Facing.EAST: Facing.WEST
            }[f]

        visited = set()
        min_x = max_x = x
        min_y = max_y = y

        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))

            min_x = min(min_x, cx)
            max_x = max(max_x, cx)
            min_y = min(min_y, cy)
            max_y = max(max_y, cy)

            if len(visited) > 6:
                return True
            for f in Facing:
                nx2, ny2 = cx, cy
                match f:
                    case Facing.NORTH: ny2 -= 1
                    case Facing.SOUTH: ny2 += 1
                    case Facing.WEST: nx2 += 1
                    case Facing.EAST: nx2 -= 1

                if not is_pos_valid(x, y, self.__bounds):
                    continue

                wall_between = (cx == x and cy == y and f == facing) or \
                    (cx == target_x and cy == target_y and
                     f == opposite(facing))

                if not grid[cx][cy].wall_request(f) or wall_between:
                    stack.append((nx2, ny2))

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        if width > 3 or height > 3:
            return True
        return False

    def generate(self) -> bool:
        rng = Random(self.__config.get(ConfigValues.SEED))
        from ..position import Position
        start: Position = self.__config.get(ConfigValues.ENTRY)
        self.crawl(start.get_x(), start.get_y(), rng)

    def crawl(self, x: int, y: int, rng: Random) -> bool:
        to_check = [f for f in Facing if self.get()[x][y].wall_request(f)]
        self.get()[x][y].is_visited = True
        print(f"x{x} y{y}")
        while to_check:
            r_face_id = rng.randint(0, len(to_check) - 1)
            r_face = to_check.pop(r_face_id)

            def get_direction(facing: Facing) -> tuple[int, int]:
                return {
                    Facing.NORTH: (0, -1),
                    Facing.SOUTH: (0, 1),
                    Facing.WEST: (-1, 0),
                    Facing.EAST: (1, 0)
                }[facing]

            dir_x, dir_y = get_direction(r_face)

            if not is_pos_valid(x + dir_x, y + dir_y, self.__bounds):
                continue
            if self.get()[x + dir_x][y + dir_y].is_visited:
                continue
            if self.would_excede_room_limit(x, y, r_face):
                continue

            def opposite(f: Facing) -> Facing:
                return {
                    Facing.NORTH: Facing.SOUTH,
                    Facing.SOUTH: Facing.NORTH,
                    Facing.WEST: Facing.EAST,
                    Facing.EAST: Facing.WEST
                }[f]

            self.get()[x][y].break_wall(r_face)
            self.get()[x + dir_x][y + dir_y].break_wall(opposite(r_face))

            self.crawl(x + dir_x, y + dir_y, rng)
        return True
