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
import torch.nn as nn
import torch
from transformers import RobertaForSequenceClassification, RobertaTokenizer, RobertaModel, RobertaConfig
from model import Seq2Seq



def transform_data(in_fname: str, out_fname: str, model_name: str):
    # takes a jsonlfile of program data as 'in_fname', and writes a "transformed" version of the program data to 'out_fname'
    config = RobertaConfig.from_pretrained('roberta-base')
    tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
    encoder = RobertaModel.from_pretrained('roberta-base',config=config)    
    decoder_layer = nn.TransformerDecoderLayer(d_model=config.hidden_size, nhead=config.num_attention_heads)
    decoder = nn.TransformerDecoder(decoder_layer, num_layers=6)
    model=Seq2Seq(encoder=encoder,decoder=decoder,config=config,
                  beam_size=10,max_length=512,
                  sos_id=tokenizer.cls_token_id,eos_id=tokenizer.sep_token_id)
    device = torch.device('cpu')
    model.load_state_dict(torch.load(model_name, map_location = torch.device('cpu')))
    model.to(device)
    globals.model = model

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
                    target, POP_SIZE, TEMP, BUDGET, EARLY_STOPPING, model
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
    transform_data("example_input.jsonl", "transformed_4.csv", "roberta/python/checkpoint-best-bleu/pytorch_model.bin")
