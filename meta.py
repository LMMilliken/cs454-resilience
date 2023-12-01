import copy
from ga.ga import ga
from ga import globals
from utils.utils import load_model
from utils.config import *
import json
from tqdm import tqdm


def transform_data(in_fname: str, out_fname: str, model_name: str):
    # takes a jsonlfile of program data as 'in_fname', and writes a "transformed" version of the program data to 'out_fname'
    globals.model = load_model(model_name)

    print("STARTING METAMORPHIC TRANSFORMATIONS")

    with open(in_fname, "r") as in_file, open(out_fname, "w") as out_file:
        for line in tqdm(in_file):
            adversary = copy.deepcopy(json.loads(line))
            adversary["code"] = ga(adversary, POP_SIZE, TEMP, BUDGET, EARLY_STOPPING)
            out_file.write(json.dumps(adversary) + "\n")
