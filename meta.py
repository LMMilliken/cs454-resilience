import copy
from ga.ga import ga
from ga import globals
from utils.utils import load_model
from utils.config import *
from fitness.fitness import generate_docstring, extract_docstring_and_content
import csv
import json
from tqdm import tqdm
from libcst._exceptions import ParserSyntaxError


def transform_data(in_fname: str, out_fname: str, model_name: str):
    # takes a jsonlfile of program data as 'in_fname', and writes a "transformed" version of the program data to 'out_fname'
    globals.model = load_model(model_name)

    print("STARTING METAMORPHIC TRANSFORMATIONS")

    with open(in_fname, "r") as in_file, open(out_fname, "w") as out_file:
        writer = csv.writer(out_file)
        for i, line in enumerate(in_file):
            line_dict = json.loads(line)
            print(i)
            target = line_dict["code"]
            globals.expected_out = line_dict["docstring"]
            try:
                adversary = ga(
                    target, POP_SIZE, TEMP, BUDGET, EARLY_STOPPING, model_name
                )
                mt = ""
                for s in adversary[1]:
                    mt += str(type(s))+'/'
                guess = generate_docstring(adversary[0], model_name)
                writer.writerow([adversary[0], guess, mt])
            except ParserSyntaxError as e:
                print("program cant be parsed!")


if __name__ == "__main__":
    # transform_data("example_input.jsonl", "transformed_turbo.csv", "gpt-3.5-turbo")
    transform_data("example_input.jsonl", "transformed_4.csv", "gpt-4-1106-preview")
