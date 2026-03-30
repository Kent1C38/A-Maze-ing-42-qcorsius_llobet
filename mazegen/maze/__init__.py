from ..utils import is_pos_valid, get_42logo_cells
from ..config import Configuration
from .cell import Cell, Facing
from .visualizer import Map
from random import Random
from ..enums import Color, MazeObject
from ..position import Position
from sys import stdout, setrecursionlimit, maxsize
from os import system
from typing import Tuple

setrecursionlimit(10000)


class Maze:
    """
    The Maze class.

    This is by far the most important class of the entire program.
    A maze object contains all the logic ranging from generation algorithms, to
    solving algorithms, to exporting it as a hexadecimal representation of its
    walls.
    """

    def __init__(self, config: Configuration) -> None:
        """
        Initializes a new Maze object.

        Initializes a new Maze. The properties of the maze all depends on the
        configuration passed as parameter.

        Args:
            config (Configuration): The configuration of the maze.

        Returns:
            none (None):
        """
        self.__maze = [[Cell()
                        for _ in range(config.width)]
                       for _ in range(config.height)]
        self.__config = config
        self.__visualizer = Map(config)

        self.__solved = False
        self.__visualizer.add_entry(config.entry_pos)
        self.__visualizer.add_exit(config.exit_pos)
        self.__generate: bool = False
        self.__anim_maze: bool = False
        self.__anim_path: bool = False

    def get(self) -> list[list[Cell]]:
        """
        Returns the maze.

        Returns the maze with all its cells.

        Args:
            none (None):

        Returns:
            maze (list[list[Cell]]): The maze.
        """
        return self.__maze

    def convert_to_hex_str(self) -> str:
        """
        Convers the walls to hexadecimal representation.

        This is useful to export the maze into the output file.

        Args:
            none (None):

        Returns:
            hex (str): The hexadecimal representation.
        """
        string = ""
        lab: list[list[Cell]] = self.__maze
        for line in lab:
            for cell in line:
                string += f"{cell.get_active_walls():x}".upper() \
                    if cell else "0"
            string += "\n"
        return string

    def gen_ft_logo(self) -> None:
        """
        Generates the 42 logo.

        The size of the logo does not change. The position however varies
        depending on the size of the maze, but will always stay at the center.

        Args:
            none (None):

        Returns:
            none (None):
        """
        x_center = self.__config.width // 2
        y_center = self.__config.height // 2
        start = Position(x=x_center - 3, y=y_center - 2)
        logo_cells = get_42logo_cells(
            self.__config.width, self.__config.height)

        for p in logo_cells:
            self.get()[p[1]][p[0]].set_unbreakable(True)
        self.__visualizer.add_ft(start.x, start.y)

    def would_excede_room_limit(self, x: int, y: int, facing: Facing) -> bool:
        """
        Checks if breaking a cell would make a too large room.

        Takes the position of a cell and checks on all sides if breaking the
        walls would make a room too large. Returns True if too large, False
        otherwise.

        Args:
            x (int): The X coordinate of the cell.
            y (int): The Y coordinate of the cell.
            facing (Facing): An enum for the walls.

        Returns:
            bool (bool): True if would be too large, False otherwise.
        """
        grid = self.get()
        target_x = x + facing.dx
        target_y = y + facing.dy

        def opposite(f: Facing) -> Facing:
            """
            Returns the opposite walls.

            Checks all the walls and returns its opposite.

            Args:
                f (Facing): The wall.

            Returns:
                f (Facing): The opposite sides.
            """
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
                if not is_pos_valid(nx, ny, self.get_bounds()):
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

    def generate(self, keep_seed: bool = False,
                 invert_solve: bool = False) -> bool:
        """
        Generates a new maze.

        This is the main function that generates a maze. It orchestrates the
        whole process and returns True if everything went well.

        Args:
            keep_seed (bool): Whether to keep the previous seed or not.
            invert_solve (bool): Accounts for the path solving.

        Returns:
            bool (bool): True if everything went well.
        """
        self.reset()
        if not keep_seed:
            self.new_rand_seed()
        rng = Random(self.__config.seed)

        self.gen_ft_logo()

        start: Position = self.__config.entry_pos

        system("clear")
        self.__visualizer.reset()
        self.__visualizer.add_walls(self.convert_to_hex_str())
        if self.__anim_maze and not invert_solve:
            self.visualize()
        self.crawl(start.x, start.y, rng, invert_solve)

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
                                            self.get_bounds()):
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
        from .solver import a_star
        self.__visualizer.reset()
        self.__visualizer.add_entry(self.__config.entry_pos)
        self.__visualizer.add_exit(self.__config.exit_pos)
        self.__visualizer.add_walls(self.convert_to_hex_str())
        path = a_star(self.get(), self.__config.entry_pos,
                      self.__config.exit_pos)

        if not path:
            return False
        if invert_solve:
            self.__solved = not self.__solved
        if self.__solved and path and not self.__anim_path:
            self.__visualizer.add_path(
                self.__config.entry_pos.x,
                self.__config.entry_pos.y,
                path
            )

        self.__generate = True
        self.gen_ft_logo()

        if self.__solved and path and self.__anim_path:
            self.visualize()
            self.__visualizer.add_path(
                self.__config.entry_pos.x,
                self.__config.entry_pos.y,
                path
            )
            self.__visualizer.animate_path()
        stdout.flush()

        with open(self.__config.output_file, "w") as o_file:
            o_file.write(self.convert_to_hex_str())
            o_file.write("\n")
            entry = self.__config.entry_pos
            o_file.write(f"\n{entry.x},{entry.y}")
            exitt = self.__config.exit_pos
            o_file.write(f"\n{exitt.x},{exitt.y}")
            o_file.write("\n" + path)

        return True

    def crawl(self, x: int, y: int, rng: Random,
              path_solve: bool = False) -> bool:
        """
        Carves path in the maze.

        This is one of the functions that does the maze generation algorithm.
        It will carve out the pathways in the maze recursively. This is more
        commonly known as Recursive Backtracking.

        Args:
            x (int): The X coordinate of the current cell.
            y (int): The Y coordinate of the current cell.
            rng (Random): Dictates which way the algorithm goes.
            path_solve (bool): Sets if the crawl animation should play or not.

        Returns:
            bool (bool): Returns True if everything went well.
        """
        self.get()[y][x].is_visited = True
        directions = [f for f in Facing if self.get()[y][x].wall_request(f)]
        while directions:
            f = directions.pop(rng.randint(0, len(directions) - 1))
            nx, ny = x + f.dx, y + f.dy

            if not is_pos_valid(nx, ny, self.get_bounds()):
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

            if self.__anim_maze and not path_solve:
                walls: int = self.get()[y][x].get_active_walls()

                self.__visualizer.animate_maze(walls, x, y,
                                               self.__config.width,
                                               self.__config.height)
            self.crawl(nx, ny, rng, path_solve)
        return True

    def new_rand_seed(self) -> None:
        """
        Sets a new random seed.

        Sets the seed of the maze to a new random seed.

        Args:
            none (None):

        Returns:
            none (None):
        """
        rand = Random(self.__config.seed)
        self.__config.seed = rand.randint(-maxsize - 1, maxsize)

    def reset_visited(self) -> None:
        """
        Sets all cells to not visited.

        This is used to reset the maze and allow a new generation of that maze.

        Args:
            none (None):

        Returns:
            none (None):
        """
        for line in self.get():
            for cell in line:
                cell.is_visited = True

    def reset(self) -> None:
        """
        Resets the maze.

        Resets all the cells on the maze and reinitializes the maze map with
        width and height from the config.

        Args:
            none (None):

        Returns:
            none (None):
        """
        for line in self.get():
            for cell in line:
                cell.reset()
        self.__maze = [[Cell()
                        for _ in range(self.__config.width)]
                       for _ in range(self.__config.height)]
        self.__visualizer.reset()

    def visualize(self) -> None:
        """
        Calls the visualize method from the visualizer.

        As you do not have access to the visualizer object. This method calls
        its method instead.

        Args:
            none (None):

        Returns:
            none (None):
        """
        self.__visualizer.visualize()

    def set_color(self, obj: MazeObject, color: Color) -> None:
        """
        Sets the color of a maze object.

        Takes a maze object and sets its color to the specified color.

        Args:
            obj (MazeObject): The maze object.
            color (Color): An enum representing a Color.

        Returns:
            none (None):
        """
        maze_anim: bool = self.__anim_maze
        path_anim: bool = self.__anim_path

        self.__visualizer.change_color(obj, color)
        self.__anim_maze = False
        self.__anim_path = False
        if self.__generate:
            self.generate(True)
            self.__anim_maze = maze_anim
            self.__anim_path = path_anim

    def switch_animation_state(self, obj: MazeObject) -> None:
        """
        Switches the animation state of a maze object.

        Inverts the animation state of the specified object.

        Args:
            obj (MazeObject): The maze object.

        Returns:
            none (None):
        """
        match obj.value:
            case "Walls":
                self.__anim_maze = not self.__anim_maze
            case "Path":
                self.__anim_path = not self.__anim_path

    def get_animation_state(self, obj: MazeObject) -> bool:
        """
        Gets the animation state of a maze object.

        Returns the animation state of the maze objects like the walls and
        path.

        Args:
            obj (MazeObject): The maze object.

        Returns:
            state (bool): The state of the object.
        """
        match obj.value:
            case "Walls":
                return self.__anim_maze
            case "Path":
                return self.__anim_path
            case _:
                return False

    def get_status(self) -> bool:
        """
        Returns the status of the maze.

        If this returns True, that means the maze has been generated already,
        False otherwise.

        Args:
            none (None):

        Returns:
            status (bool): The state of the maze.
        """
        return self.__generate

    def hide(self) -> None:
        """
        Sets the maze to be hidden.

        Sets the state of the maze to be hidden. If hidden, the visualizer will
        not display it.

        Args:
            none (None):

        Returns:
            none (None):
        """
        self.__generate = False

    def get_config(self) -> Configuration:
        """
        Gets the configuration of the maze.

        Returns the configuration used internally by the maze.

        Args:
            none (None):

        Returns:
            config (Configuration): The configuration of the maze.
        """
        return self.__config

    def get_bounds(self) -> Tuple[int, int]:
        """
        Gets the bounds of the maze.

        Returns the width and height of the maze as a tuple.

        Args:
            none (None):

        Returns:
            bounds (Tuple[int, int]): The bounds of the maze.
        """
        return (self.__config.width, self.__config.height)

    def get_colors(self) -> Tuple[Color, Color, Color, Color, Color]:
        """
        Returns the colors used to display the maze.

        Used for UI.

        Args:
            none (None):

        Returns:
            colors (Tuple): Colors
        """
        return self.__visualizer.get_colors()
