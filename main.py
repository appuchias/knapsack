from argparse import ArgumentParser, Namespace
import random

from models import Thing, Solution

MAX_GENERATIONS: int = 100
MAX_WEIGHT: int = 25
MUTATION_RATE: float = 0.05


def main(fp: str) -> None:
    things: list[Thing] = list()

    with open(fp) as f:
        for line in f.readlines():
            name, weight, value = line.split(";")
            things.append(Thing(name, int(weight), int(value)))

    print("Gen | Weight | Value | Best solution")

    # Run the genetic algorithm
    solutions = list()
    for generation_num in range(MAX_GENERATIONS):
        solutions = genetic_algorithm(things, solutions)

        # Print the top solution
        top_solution = solutions[0]
        print(
            f"{generation_num:>3} | {top_solution.weight(things):^6} | {top_solution.value(things):^5} | {str(top_solution)}"
        )


def genetic_algorithm(things: list[Thing], solutions: list[Solution]) -> list[Solution]:
    """Runs the genetic algorithm.

    This is done by creating a new generation of solutions and selecting the
    best ones.
    """

    # Create a new generation of solutions and sort them by fitness
    new_solutions = new_generation(things, solutions)
    new_solutions.sort(key=lambda x: x.fitness(things, MAX_WEIGHT), reverse=True)

    return new_solutions


def new_generation(things: list[Thing], solutions: list[Solution]) -> list[Solution]:
    """Selects the new generation of solutions.

    This is done by using elitism, crossover and mutation. The amount of
    solutions in the new generation is equal to the population size. If no
    population size is given, the length of solutions is used.
    """

    # First generation
    if not solutions:
        length = len(things)
        return [
            Solution([random.random() >= 0.5 for _ in range(length)])
            for _ in range(length)
        ]

    # Subsequent generations
    new_generation = list()
    population_size = len(solutions)

    # Elitism
    elitism = 2 if population_size > 2 and population_size % 2 == 0 else 1
    top_solutions = sorted(
        solutions, key=lambda x: x.fitness(things, MAX_WEIGHT), reverse=True
    )[:elitism]
    new_generation.extend(top_solutions)

    # Crossover
    while len(new_generation) < population_size:
        weights = [s.fitness(things, MAX_WEIGHT) for s in solutions]
        if sum(weights) == 0:
            weights = [1 for _ in weights]

        parents = tuple(random.choices(solutions, weights=weights, k=2))
        children = [mutation(c) for c in crossover(parents)]

        new_generation.extend(children)

    return new_generation


def crossover(parents: tuple[Solution, Solution]) -> tuple[Solution, Solution]:
    """Crossover two solutions to get the 'children'.

    This is done by selecting a random index and swapping the bits after that
    index from the two parents.
    """

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

    if mut != solution:
        print("Mutation:", solution, "->", mut)

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
