import copy
from ga.ga import ga
from ga import globals
from utils.utils import load_model
from utils.config import *
from utils.notify import notify
from fitness.fitness import generate_docstring, extract_docstring_and_content
import argparse
import csv
import json
from tqdm import tqdm
from libcst._exceptions import ParserSyntaxError


def transform_data(in_fname: str, out_fname: str, model_name: str, alias: str = ""):
    # takes a jsonlfile of program data as 'in_fname', and writes a "transformed" version of the program data to 'out_fname'
    globals.model = load_model(model_name)

    print("STARTING METAMORPHIC TRANSFORMATIONS")
    notify(f"{alias} - STARTING METAMORPHIC TRANSFORMATIONS", "let_me_know")
    try:
        with open(in_fname, "r") as in_file, open(out_fname, "w") as out_file:
            writer = csv.writer(out_file)
            num_lines = sum(1 for _ in in_file)
            for i, line in enumerate(in_file):
                if i == num_lines // 10:
                    notify(f"{alias} - {i} / {num_lines} transformed")
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
                        mt += str(type(s)) + "/"
                    guess = generate_docstring(adversary[0], model_name)
                    writer.writerow([adversary[0], guess, mt])
                except ParserSyntaxError as e:
                    print("program cant be parsed!")
    except Exception as e:
        notify(f"{alias} - ERROR:\n{e}", "let_me_know")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--in_fname",
        default="None",
        type=str,
        required=True,
        help="name of file containing original programs",
    )
    parser.add_argument(
        "--out_fname",
        default=None,
        type=str,
        required=True,
        help="name of file to write outputs to",
    )
    parser.add_argument(
        "--model_name",
        default=None,
        type=str,
        required=True,
        help="name of the model to use in fitness function",
    )
    parser.add_argument(
        "--alias",
        default="",
        type=str,
        required=True,
        help="alias to be used in logging",
    )

    args = parser.parse_args()

    transform_data(args.in_fname, args.out_fname, args.model_name, args.alias)
