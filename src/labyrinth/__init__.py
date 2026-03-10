from ..utils import is_pos_valid
from ..config import Configuration, ConfigValues
from .cell import Cell, Facing
from random import Random


class Labyrinth:
    def __init__(self, config: Configuration, debug: bool = False):
        self.__maze = [[Cell(True, True, True, True)
                        for _ in range(config.get(ConfigValues.HEIGHT))]
                       for _ in range(config.get(ConfigValues.WIDTH))]
        self.__config = config
        self.__bounds = (self.__config.get(ConfigValues.WIDTH),
                         self.__config.get(ConfigValues.HEIGHT))
        self.debug = debug

    def get(self) -> list[list[Cell]]:
        return self.__maze

    def set_cell(self, x: int, y: int, cell: Cell):
        if is_pos_valid(x, y, self.__bounds):
            self.__maze[x][y] = cell
        else:
            raise Exception(
                f"Could not set cell at ({x},{y}): invalid position!")

    def convert_to_hex_str(self) -> str:
        string = ""
        lab: list[list[Cell]] = self.__maze
        for line in lab:
            for cell in line:
                string += f"{cell.get_active_walls():x}".upper() \
                    if cell else "0"
            string += "\n"
        return string

    def would_excede_room_limit(self, x: int, y: int, facing: Facing):
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

        # Compter seulement les cellules avec 2 murs cassés ou plus
            cell = grid[cx][cy]
            open_walls = 4 - cell.get_active_walls().bit_count()
            if open_walls < 2:
                continue  # c'est un couloir étroit, ne bloque pas

        # Si la pièce devient trop grande
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

    def generate(self) -> bool:
        rng = Random(self.__config.get(ConfigValues.SEED))
        from ..position import Position
        start: Position = self.__config.get(ConfigValues.ENTRY)
        if self.debug:
            print(f"Starting labyrinth generation at ({
                  start.get_x()},{start.get_y()})")
        self.crawl(start.get_x(), start.get_y(), rng)

    def crawl(self, x: int, y: int, rng: Random) -> bool:
        self.get()[x][y].is_visited = True
        if self.debug:
            print(f"Visiting cell ({x},{y})")

        directions = [f for f in Facing if self.get()[x][y].wall_request(f)]
        while directions:
            f = directions.pop(rng.randint(0, len(directions) - 1))
            nx, ny = x + f.dx, y + f.dy

            if not is_pos_valid(nx, ny, self.__bounds):
                if self.debug:
                    print(f"  Skipping ({nx},{ny}): out of bounds")
                continue

            if self.get()[nx][ny].is_visited:
                if self.debug:
                    print(f"  Skipping ({nx},{ny}): already visited")
                continue

            if self.would_excede_room_limit(x, y, f):
                if self.debug:
                    print(f"  Skipping ({nx},{ny}): would exceed room limit")
                continue

            self.get()[x][y].break_wall(f)
            self.get()[nx][ny].break_wall({
                Facing.NORTH: Facing.SOUTH,
                Facing.SOUTH: Facing.NORTH,
                Facing.WEST: Facing.EAST,
                Facing.EAST: Facing.WEST
            }[f])

            if self.debug:
                print(f"  Breaking wall {
                      f.name} between ({x},{y}) and ({nx},{ny})")

            self.crawl(nx, ny, rng)

        return True
