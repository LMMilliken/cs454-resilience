import random
import time
from ga import globals
from typing import Any, Dict
from libcst import parse_expression

from ga.solution import Solution


def ga(
    target: Dict[str, Any], pop_size: int, temp: float, budget: int, early_stopping: int
):
    start_time = time.time()
    globals.original = parse_expression(target["code"])
    globals.expected_out = target["docstring"]

    population = sorted([Solution() for _ in range(pop_size)], key=lambda x: x.fitness)
    fittest = population[0]
    stagnant = 0
    while time.time() - start_time < budget and stagnant < early_stopping:
        population = repopulate(population, temp)
        new_fittest = population[0]
        if new_fittest.fitness > fittest.fitness:
            stagnant = 0
            fittest = new_fittest
        else:
            stagnant += 1
    return str(fittest)


def repopulate(population, temp):
    next_gen = []
    while len(next_gen) < len(population):
        p1 = sorted(random.choices(population, k=4), key=lambda x: x.fitness)[0]
        p2 = sorted(random.choices(population, k=4), key=lambda x: x.fitness)[0]
        c1, c2 = Solution.crossover(p1, p2)
        c1.mutate(temp)
        c2.mutate(temp)
        next_gen.append(c1)
        next_gen.append(c2)
    return sorted(population + next_gen, key=lambda x: x.fitness)[: len(population)]
