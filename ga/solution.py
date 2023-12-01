import random
from typing import List, Tuple
from libcst import CSTNode
from ga import globals
from lampion.transformers.basetransformer import BaseTransformer
import copy


class Solution:
    def __init__(self, transformers: List[BaseTransformer]) -> None:
        self.transformers = transformers
        # TODO: define structure of solution
        self._fitness = None

    def __str__(self) -> str:
        # turn solution back into regular code
        cst = self.apply()
        return cst.code

    @property
    def fitness(self):
        if self._fitness is None:
            self._fitness = self.calculate_fitness()
        return self._fitness

    def calculate_fitness(self) -> float:
        # TODO: implement fitness function
        pass

    def mutate(self, temp: float):
        # TODO: implement mutation
        # JUST DO WHAT THEY SAY IN THE PAPER, EZ
        pass

    def apply(self) -> CSTNode:
        # let each transformer run "apply" once so that we know the index of the node that it changes
        for transformer in self.transformers:
            transformer.apply(copy.deepcopy(globals.original))
            transformer.reset()

        # Sort the transformrs by largest index to smallest
        self.transformers = sorted(
            list(
                filter(lambda transformer: transformer.node_count is not None),
                self.transformers,
            ),
            key=lambda transformer: transformer.node_count,
            reverse=True,
        )
        ret = copy.deepcopy(self.original)
        for transformer in self.transformers:
            ret = transformer.apply(ret)
            transformer.reset()
        return ret

    def crossover(p1: "Solution", p2: "Solution") -> Tuple["Solution", "Solution"]:
        # 1 place crossover for now, cba to do multi point.
        transformers_1 = copy.deepcopy(p1.transformers)
        transformers_2 = copy.deepcopy(p2.transformers)

        pivot1 = random.randint(0, len(transformers_1) - 1)
        pivot2 = random.randint(0, len(transformers_2) - 1)

        c1 = Solution(transformers_1[:pivot1] + transformers_2[pivot2:])
        c2 = Solution(transformers_2[:pivot2] + transformers_1[pivot1:])
        return c1, c2
