from argparse import ArgumentParser
from typing import Callable, Any

from models import Thing


def main(fp: str) -> None:
    things = list()

    with open(fp) as f:
        for line in f.readlines():
            name, weight, value = line.split(";")
            things.append(Thing(name, int(weight), int(value)))

    print(things)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input", type=str, help="Input file")

    main(parser.parse_args().input)
