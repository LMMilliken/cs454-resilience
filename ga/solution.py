from typing import Tuple
from libcst import CSTNode
import copy


class Solution:
    def __init__(self, original: CSTNode) -> None:
        self.original = original
        self.adversary = copy.deepcopy(self.original)
        # TODO: define structure of solution
        self._fitness = None

    def __str__(self) -> str:
        # TODO: write method to turn solution back into regular code
        pass

    @property
    def fitness(self):
        if self._fitness is None:
            self._fitness = self.calculate_fitness()
        return self._fitness

    def calculate_fitness(self):
        # TODO: implement fitness function
        pass

    def mutate(self):
        # TODO: implement mutation
        pass

    def crossover(p1: "Solution", p2: "Solution") -> Tuple["Solution", "Solution"]:
        # TODO: implement once structure of Solution has been defined
        pass

    @classmethod
    def generate(cls) -> "Solution":
        # TODO: implement once structure of Solution has been defined
        # Generates a new candidate solution
        pass
