from ..position import Position
from .cell import Cell, Facing
import heapq


class Node:
    """
    The Node class.

    Nodes are primarily used for the solver algorithm, which in our case is
    A*. It is easier to work with nodes than to directly use the cell structure
    of our maze, as it is not very compatible with the algorithm.
    """
    def __init__(self, x: int, y: int, cost_from_start: int,
                 goal: Position) -> None:
        """
        Initializes a new Node object.

        Creates, initializes and returns a new Node object. Nodes are primarily
        used for the A* algorithm.

        Args:
            x (int): The X coordinate of the node.
            y (int): The Y cooddinate of the node.
            cost_from_start (int): The distance between the node and the start.
            goal (Position): The coordinates of the end goal.

        Returns:
            none (None):
        """
        self.coords = Position(x=x, y=y)
        self.cost_from_start = cost_from_start
        self.estimated_distance = self.coords.heuristic(goal)
        self.total_cost = self.cost_from_start + self.estimated_distance
        self.parent: Node | None = None

    def set_parent(self, parent: "Node") -> None:
        """
        Sets the parent of the node.

        Used for the A* algorithm.

        Args:
            parent (Node): The node to parent itself to.

        Returns:
            none (None):
        """
        self.parent = parent

    @property
    def x(self) -> int:
        return self.coords.x

    @property
    def y(self) -> int:
        return self.coords.y


def get_valid_neighbors(maze: list[list[Cell]],
                        position: Position) -> list[Position]:
    """
    Checks for neighbors cells.

    This is used to check whether the cells nearby can be accessed or not.

    Args:
        maze (list[list[Cell]]): The cells of the maze.
        position (Position): The coordinates of cell to perform the check on.

    Returns:
        valid (list[Position]): The valid cells.
    """
    neighbours = []
    for direction in [f for f in Facing if not
                      maze[position.y][position.x].wall_request(f)]:
        neigh = Position(x=position.x + direction.dx,
                         y=position.y + direction.dy)
        neighbours.append(neigh)

    return neighbours


def a_star(maze: list[list[Cell]], start: Position,
           goal: Position) -> str | None:
    """
    The pathfinding algorithm to solve the maze.

    It takes all maze cells and checks for the distance between the cells and
    the exit. By computing this distance and the distance needed to go to
    said cell, it will choose the path with the least distance, thus finding
    the shortest path to the exit.

    Args:
        maze (list[list[Cell]]): Cells of the maze.
        start (Position): The coordinates of the entry point.
        goal (Position): The coordinates of the exit point.

    Returns:
        path (str | None): Returns the path if solved, None otherwise.
    """
    start_node = Node(start.x, start.y, 0, goal)

    counter = 0
    open_list = [(start_node.total_cost, counter, start_node)]
    open_dict = {start.get(): start_node}
    closed_set = set()

    while open_list:
        _, _, current_node = heapq.heappop(open_list)
        current_pos: Position = current_node.coords
        curr_node: Node = open_dict[current_pos.get()]

        if current_pos.get() == goal.get():
            return reconstruct_path(curr_node)

        closed_set.add(current_pos.get())

        for neighbor_pos in get_valid_neighbors(maze, current_pos):
            key = neighbor_pos.get()

            if key in closed_set:
                continue

            tentative_cost = curr_node.cost_from_start + 1

            if key not in open_dict:
                neighbor = Node(
                    neighbor_pos.x,
                    neighbor_pos.y,
                    tentative_cost,
                    goal
                )
                neighbor.set_parent(current_node)

                open_dict[key] = neighbor
                counter += 1
                heapq.heappush(
                    open_list, (neighbor.total_cost, counter, neighbor))

            else:
                neighbor = open_dict[key]

                if tentative_cost < neighbor.cost_from_start:
                    neighbor.cost_from_start = tentative_cost
                    neighbor.total_cost = (tentative_cost +
                                           neighbor.estimated_distance)
                    neighbor.set_parent(current_node)

                    counter += 1
                    heapq.heappush(
                        open_list, (neighbor.total_cost, counter, neighbor))
    return None


def reconstruct_path(goal_node: Node) -> str | None:
    """
    Returns the full path to the exit node.

    Args:
        goal_node (None): The node to reach.

    Returns:
        path (str | None): Returns str if path is valid, None otherwise.
    """
    path = ""
    current = goal_node

    while current.parent is not None:
        vec = (current.x - current.parent.x, current.parent.y - current.y)
        if vec == Facing.SOUTH.vector:
            path += "N"
        elif vec == Facing.NORTH.vector:
            path += "S"
        elif vec == Facing.WEST.vector:
            path += "W"
        elif vec == Facing.EAST.vector:
            path += "E"
        else:
            return None
        current = current.parent

    return path[::-1]
