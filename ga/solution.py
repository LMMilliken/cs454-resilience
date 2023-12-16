import random
from typing import List, Tuple
from libcst import CSTNode
from ga import globals
from lampion import (
    AddVariableTransformer,
    AddCommentTransformer,
    RenameVariableTransformer,
    RenameParameterTransformer,
    LambdaIdentityTransformer,
    AddNeutralElementTransformer,
    IfTrueTransformer,
    IfFalseElseTransformer,
    ForOneTransformer,
    WhileTrueTransformer,
    BaseTransformer,
)
from fitness.fitness import (
    generate_docstring,
    calculate_bleu_score,
    extract_docstring_and_content,
    generate_bert_docstring
)
import copy


class Solution:
    def __init__(
        self, transformers: List[BaseTransformer] = [], max_transformations: int = 5
    ) -> None:
        self.transformers = transformers[:max_transformations]
        self.max_transformations = max_transformations
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
        _, code = extract_docstring_and_content(file_path="", file_content=str(self))
        #generated_docstring = generate_docstring(code, model=globals.model)
        generated_docstring = generate_bert_docstring(code, model = globals.model)
        return calculate_bleu_score(generated_docstring, globals.expected_out)

    def mutate(self, temp: float):
        # TODO: implement mutation
        # temp chance of adding new transformation, and 1-temp chance of deleting a random transformation
        if random.random() < temp:
            if len(self.transformers) <= 1 or (
                random.random() < 0.8
                and len(self.transformers) < self.max_transformations
            ):
                choice = [
                    "AddUnusedVariableTransformer",
                    "AddCommentTransformer",
                    "RenameVariableTransformer",
                    "RenameParameterTransformer",
                    "LambdaIdentityTransformer",
                    "AddNeutralElementTransformer",
                    "IfTrueTransformer",
                    "IfFalseElseTransformer",
                    "ForOneTransformer",
                    "WhileTrueTransformer",
                ]
                chosen = random.choice(choice)
                # bit lengthy and unconcise, but better than initiating 10 transformer every mutation
                match chosen:
                    case "AddUnusedVariableTransformer":
                        new = AddVariableTransformer(string_randomness="full")
                    case "AddCommentTransformer":
                        new = AddCommentTransformer(string_randomness="full")
                    case "RenameVariableTransformer":
                        new = RenameVariableTransformer(string_randomness="full")
                    case "RenameParameterTransformer":
                        new = RenameParameterTransformer(string_randomness="full")
                    case "LambdaIdentityTransformer":
                        new = LambdaIdentityTransformer()
                    case "AddNeutralElementTransformer":
                        new = AddNeutralElementTransformer()
                    case "IfTrueTransformer":
                        new = IfTrueTransformer()
                    case "IfFalseElseTransformer":
                        new = IfFalseElseTransformer()
                    case "ForOneTransformer":
                        new = ForOneTransformer()
                    case "WhileTrueTransformer":
                        new = WhileTrueTransformer()
                self.transformers.append(new)
            else:
                self.transformers.pop(random.randrange(0, len(self.transformers)))

    def apply(self) -> CSTNode:
        # let each transformer run "apply" once so that we know the index of the node that it changes
        for transformer in self.transformers:
            transformer.apply(copy.deepcopy(globals.original))
            transformer.reset()

        # Sort the transformrs by largest index to smallest
        self.transformers = sorted(
            list(
                filter(
                    (lambda transformer: transformer.node_count is not None),
                    self.transformers,
                ),
            ),
            key=lambda transformer: transformer.node_count,
            reverse=True,
        )
        ret = copy.deepcopy(globals.original)
        for transformer in self.transformers:
            ret = transformer.apply(ret)
            transformer.reset()
        return ret

    def crossover(p1: "Solution", p2: "Solution") -> Tuple["Solution", "Solution"]:
        # 1 place crossover for now, cba to do multi point.
        transformers_1 = copy.deepcopy(p1.transformers)
        transformers_2 = copy.deepcopy(p2.transformers)

        if len(transformers_1) == 0 or len(transformers_2) == 0:
            child_transformers_1 = transformers_1 + transformers_2
            child_transformers_2 = transformers_1 + transformers_2
        else:
            pivot1 = random.randrange(0, len(transformers_1))
            pivot2 = random.randrange(0, len(transformers_2))

            child_transformers_1 = transformers_1[:pivot1] + transformers_2[pivot2:]
            child_transformers_2 = transformers_2[:pivot2] + transformers_1[pivot1:]
            random.shuffle(child_transformers_1)
            random.shuffle(child_transformers_2)

        c1 = Solution(child_transformers_1)
        c2 = Solution(child_transformers_2)
        return c1, c2

    @staticmethod
    def generate_population(pop_size: int, max_transformations: int):
        pop = [
            Solution(max_transformations=max_transformations) for _ in range(pop_size)
        ]
        for sol in pop:
            sol.mutate(1.0)
        return pop
