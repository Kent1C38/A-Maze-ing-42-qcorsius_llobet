from sys import argv
from .config import Configuration, ConfigValues
from .labyrinth import Labyrinth
from visualizer import Map

if __name__ == "__main__":
    if len(argv) <= 1:
        print(f"Usage: python3 {argv[0]} <config file path>")
    else:
        config_path = argv[1]
        config = Configuration(config_path)

        lab = Labyrinth(config, debug=False)

        lab.generate()

        visu = Map(config.get(ConfigValues.WIDTH),
                   config.get(ConfigValues.HEIGHT))

        visu.add_walls(lab.convert_to_hex_str())
        visu.visualize()
