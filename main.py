from argparse import ArgumentParser, Namespace
import random
from rich.console import Console
from rich.table import Table
from rich import print

from models import Thing, Solution

MAX_GENERATIONS: int = 100
MAX_WEIGHT: int = 25
MUTATION_RATE: float = 0.01


def main(fp: str) -> None:
    things: list[Thing] = list()

    with open(fp) as f:
        for line in f.readlines():
            name, weight, value = line.split(";")
            things.append(Thing(name, int(weight), int(value)))

    # Run the genetic algorithm
    top_solutions = genetic_algorithm(things)

    c = Console()
    table = Table(show_header=True, header_style="bold white")
    table.add_column("Gen.", justify="center", style="cyan")
    table.add_column("Weight", justify="center", style="magenta")
    table.add_column("Value", justify="center", style="green")
    table.add_column("Best solution", justify="left", style="blue")

    for gen, solution in enumerate(top_solutions):
        table.add_row(
            str(gen),
            str(solution.weight(things)),
            str(solution.value(things)),
            str(solution),
        )
    c.print(table)


def genetic_algorithm(things: list[Thing]) -> list[Solution]:
    """Runs the genetic algorithm.

    This is done by creating a new generation of solutions and selecting the
    best solution from that generation. This process is repeated until the
    maximum amount of generations is reached.
    """

    solutions = list()
    top_solutions = list()

    for gen in range(MAX_GENERATIONS):
        print(f"Running generation #{gen:02}", end="\r")

        solutions = new_generation(things, solutions)
        solutions.sort(key=lambda x: x.fitness(things, MAX_WEIGHT), reverse=True)

        top_solution = solutions[0]
        top_solutions.append(top_solution)

    print("All generations have finished.")
    print()

    # return max(top_solutions, key=lambda x: x.fitness(things, MAX_WEIGHT))
    return top_solutions


def new_generation(things: list[Thing], solutions: list[Solution]) -> list[Solution]:
    """Creates the new generation of solutions.

    This is done by using elitism, crossover and mutation. The population size
    of the new generation is equal to the amount of things provided.
    """

    # First generation: create random solutions
    if not solutions:
        length = len(things)
        return [
            Solution([random.random() >= 0.5 for _ in range(length)])
            for _ in range(length)
        ]

    # Subsequent generations: Use elitism, crossover and mutation
    new_generation = list()
    population_size = len(things)

    # Elitism: Add the top solution to the new generation [+ mutation]
    top_solution = max(solutions, key=lambda x: x.fitness(things, MAX_WEIGHT))
    new_generation.extend([top_solution, mutation(top_solution)])

    weights = [s.fitness(things, MAX_WEIGHT) for s in solutions]
    if sum(weights) == 0:
        weights = [1 for _ in weights]

    # Crossover: Add children with mutations to the new generation
    while len(new_generation) < population_size:
        parents = tuple(random.choices(solutions, weights=weights, k=2))
        new_generation.extend([mutation(c) for c in crossover(parents)])

    return new_generation


def crossover(parents: tuple[Solution, Solution]) -> tuple[Solution, Solution]:
    """Crossover two solutions to get the 'children'.

    This is done by selecting a random index and swapping the bits after that
    index from the two parents.
    """

    if len(parents) != 2:
        raise ValueError("Crossover requires two parents")
    elif len(parents[0].bits) != len(parents[1].bits):
        raise ValueError("Parents must have the same length")

    crossover_index = random.randint(0, len(parents[0].bits) - 1)

    parent1 = Solution(
        parents[0].bits[:crossover_index] + parents[1].bits[crossover_index:]
    )
    parent2 = Solution(
        parents[1].bits[:crossover_index] + parents[0].bits[crossover_index:]
    )

    return (parent1, parent2)


def mutation(solution: Solution, mut_rate: float = MUTATION_RATE) -> Solution:
    """Mutates a solution.

    This is done by flipping a bit in the solution with a probability of
    mut_rate.
    """

    # Flip a bit with a probability of MUTATION_RATE
    mut = Solution(
        [not bit if random.random() < mut_rate else bit for bit in solution.bits]
    )

    return mut


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
        "-m",
        "--mutation",
        type=float,
        help="Mutation rate",
        default=MUTATION_RATE,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    MAX_WEIGHT = args.weight
    MAX_GENERATIONS = args.generations
    MUTATION_RATE = args.mutation

    main(args.input)
