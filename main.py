from argparse import ArgumentParser
from typing import Callable, Any
from os import environ

# from models import Thing

MAX_GENERATIONS: int = 100
MAX_WEIGHT: int = 25
MUTATION_RATE: float = 0.05
POPULATION_SIZE: int = 100


def main(fp: str) -> None:
    things = list()

    with open(fp) as f:
        for line in f.readlines():
            name, weight, value = line.split(";")
            things.append(Thing(name, int(weight), int(value)))

    print(things)


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("input", type=str, help="Input file")
    parser.add_argument(
        "-w",
        "--weight",
        type=int,
        help="Max weight",
        default=MAX_WEIGHT,
    )
    parser.add_argument(
        "-g",
        "--generations",
        type=int,
        help="Max amount of generations",
        default=MAX_GENERATIONS,
    )
    parser.add_argument(
        "-p",
        "--population-size",
        type=int,
        help="Generation size",
        default=POPULATION_SIZE,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    MAX_WEIGHT = args.weight
    environ["max_weight"] = str(MAX_WEIGHT)
    MAX_GENERATIONS = args.generations
    environ["max_generations"] = str(MAX_GENERATIONS)
    POPULATION_SIZE = args.population_size
    environ["population_size"] = str(POPULATION_SIZE)

    from models import Thing

    main(args.input)
