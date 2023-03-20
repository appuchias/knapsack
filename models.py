from dataclasses import dataclass


@dataclass
class Thing:
    name: str
    weight: int
    value: int


@dataclass(frozen=True, order=False)
class Solution:
    bits: list[bool]

    def __str__(self) -> str:
        return "".join("1" if bit else "0" for bit in self.bits)

    def fitness(self, things: list[Thing], max_weight: int) -> int:
        """Calculate the fitness of a solution.

        This takes into account the total weight and value of the things in the
        solution. If the total weight is over the max weight, the fitness is 0.
        """

        # If the total weight is over the max weight, return 0
        return self.value(things) if self.weight(things) <= max_weight else 0

    def weight(self, things: list[Thing]) -> int:
        """Calculate the total weight of a solution."""

        return sum(thing.weight * bit for thing, bit in zip(things, self.bits))

    def value(self, things: list[Thing]) -> int:
        """Calculate the total value of a solution."""

        return sum(thing.value * bit for thing, bit in zip(things, self.bits))
