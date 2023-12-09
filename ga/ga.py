import random
import time
from ga import globals
from typing import Any, Dict
from libcst import parse_module
from ga.solution import Solution
from fitness.fitness import extract_docstring_and_content


def ga(
    target: Dict[str, Any],
    pop_size: int,
    temp: float,
    budget: int,
    early_stopping: int,
    model: str,
    max_transformations: int = 5,
):
    start_time = time.time()
    code = extract_docstring_and_content(file_path="", file_content=target)[1]
    globals.original = parse_module(code)
    globals.model = model
    population = sorted(
        Solution.generate_population(pop_size, max_transformations),
        key=lambda x: x.fitness,
    )
    fittest = population[0]
    generation = 0
    stagnant = 0
    while time.time() - start_time < budget and stagnant < early_stopping:
        population = repopulate(population, temp)
        new_fittest = population[0]
        if new_fittest.fitness > fittest.fitness:
            stagnant = 0
            fittest = new_fittest
        else:
            stagnant += 1
        generation += 1
    print(f"FINISHED AFTER {generation} GENERATIONS:")
    return str(fittest)


def repopulate(population, temp):
    next_gen = []
    while len(next_gen) < len(population):
        p1 = sorted(random.choices(population, k=2), key=lambda x: x.fitness)[0]
        p2 = sorted(random.choices(population, k=2), key=lambda x: x.fitness)[0]
        c1, c2 = Solution.crossover(p1, p2)
        c1.mutate(temp)
        c2.mutate(temp)
        next_gen.append(c1)
        next_gen.append(c2)
    return sorted(population + next_gen, key=lambda x: x.fitness)[: len(population)]
