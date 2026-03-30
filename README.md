_This project has been created as part of the 42 curriculum by llobet, qcorsius_

### DESCRIPTION

The project **A-Maze-ing** is a maze generator and solver.

### STRUCTURE

The project is structured in the following way:

```
├── config.txt                          // Maze configuration
├── Makefile                            // Makefile
├── mazegen                             // Main package directory
│   ├── app.py                          // Entry point
│   ├── config.py                       // Config class and parser
│   ├── enums
│   │   ├── color.py                    // Color Enum
│   │   ├── __init__.py                 
│   │   ├── limits.py                   // Config limits
│   │   └── maze_object.py              // Used for UI
│   ├── __init__.py
│   ├── input                           // UI-related directory
│   │   ├── __init__.py
│   │   ├── input.py                    // UI displays
│   │   └── menus.py                    // UI exit points
│   ├── maze
│   │   ├── cell.py                     // Cell class, used internally for maze
│   │   ├── __init__.py
│   │   └── visualizer.py               // Maze display logic
│   ├── position.py                     // Position class utility
│   └── utils.py                        // Other utilities
├── mazegen-0.1.0-py3-none-any.whl      // Compiled package
├── mazegen-0.1.0.tar.gz                // Package archive
├── pyproject.toml                      // Project details
└── README.md                           // This file
```

### CONFIG FILE

```
WIDTH=15                // Integer [11~100]
HEIGHT=15               // Integer [9~100]
ENTRY=0,0               // Integers
EXIT=9,8                // Integers
OUTPUT_FILE=maze.txt    // valid .txt, .maze or .mf file
PERFECT=True            // Boolean: One valid path or more
SEED=7852486468         // Integer: Seed used for the maze generation (can be negative)
```

### INSTRUCTIONS

Running the command `make run` should create a virtual environment and activate
it, then download necessary dependencies if not installed and finally launch
the project.

Alternatively, you can run `make install` first then `make run`.

If you wish to run the program in debug mode, you can run `make debug`.

If you wish to build the package, make sure you have Poetry installed first,
then run `make build`.

Additionally, flake8 and mypy are present in the package. You can run the
commands `make lint` and `make lint-strict` to execute them.

Finally, once you are done working with the package and you no longer need it,
you can run `make clean`.

When changing the maze configuration in the TUI, any changes will be applied on
the next generation of the maze. Changing setting such as the seed only applies
to the next generation, not for all following generations.


### LIBRARY

To use the package as a library within another project, you can run
`pip install mazegen-x.x.x-py3-none-any.whl` or
`pip install mazegen-x.x.x.tar.gz`

The library contains all the core logic related to maze generation and path
generation.


### ALGORITHMS

#### MAZE

For the maze, we chose to use a DFS (Depth-First-Search) algorithm. The promise
of this algorithm is it goes in one direction as far as it can, then backtrack
once it finds itself into a dead end. It repeats this process until all cells
of the maze has been visited, thus completing the generation.

By default, this algorithm always generates perfect mazes. Because of this
property, when `Perfect` is `False`, it will break random walls in the maze to
create loops and new pathways.

Note that it cannot break the outer walls or the walls constituing the 42 logo
at the center of the maze.

We chose this algorithm because it sounded the most logic and useful for our
needs and it aligned well with how we would visualize an algorithm to complete
such task.

#### PATH

For the path resolution, we chose the A* algorithm. What it does is it will
check all adjacent cells and checks if they can be visited, if yes, it will
then calculate the `cost` to go there. The `cost` is the length between the
visited cell and the cell it is currently on, plus the length between the visited
cell and the exit point. The cell with the lowest cost will be chosen and it
repeats this process until it eventually reaches the end.

We chose this algorithm because it is an algorithm that returns the shortest
path to the destination.


### RESOURCES

AI was used for mostly debugging and to seek information regarding how packaging
works with Poetry.

### CONTRIBUTIONS AND MANAGEMENT

* #### LLOBET
    * Redacting the README.md file
    * All UI systems
    * Visualizer logic
    * Documentation
    * Makefile

* #### QCORSIUS
    * Maze logic and algorithms
    * Parsing and configuration
    * Path solving algorithm
    * Packaging
    * Makefile

* #### MANAGEMENT

    Before starting the project, we settled on using TUI for the rendering of
    the maze. We did this choice because we heard that using the provided
    library was not simple and had some issues. We also thought working on a 
    TUI application was somewhat easier and would also allow us to learn more
    about how the terminal render text. (Additionally, while this is my personal
    opinion, but I believe TUI applications look very nice)

    Our vision of the project did not really change as time went by. The only
    significant changes were regarding the structure of the project and the
    UI.

    During the development of the project, some things could be improved, like
    working more regularly on it instead of rushing in a few days. While we
    did try to do this, due to the Python Modules, we had to focus on many
    tasks at once, which was not optimal.

    Despite that, we believe we did a good job regarding the development. We
    both knew what we needed to work on, we were not confused on what direction
    to take next at any point in the project. Communication between us was good
    as well, we would regularly update each other on what tasks were done and
    what to focus on next.

    We used tools to help us with some parts of the project. The most notable
    tool is Pydantic. Before we did Python Module 09, we did not know about
    Pydantic, and we would add many manual checks to ensure the configuration
    file was good. But because of that, the code was not very clean nor readable.
    So we then scrapped this part of the code and rewrote it with Pydantic in
    mind. This helped us a lot with parsing.
