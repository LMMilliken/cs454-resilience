import os
import re
from typing import Optional
from openai import OpenAI
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from transformers import RobertaModel, RobertaTokenizer, RobertaConfig
import json
import torch

# with open("key.txt", "r") as file:
#     api = file.read()
# os.environ["OPENAI_API_KEY"] = api
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_docstring(code, model: str = "gpt-3.5-turbo"):
    prompt = f"""Code: {code}\n\n# You are given a python code. Your task is to go through the code and 
    generate natural language comments explaining what the code does.
    Think of it as writing a docstring for the code. Also avoid using the function name. 
    Instead of explaining in details, just provide a high level idea.
    Make sure to keep the responses within 30 words (THIS IS MANDATORY). Start like this:
    This function ……..\n"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f""},
        ],
    )
    return response.choices[0].message.content



def calculate_bleu_score(predictions, references):
    original_tokens = references.split()
    transformed_tokens = predictions.split()
    smoothing = SmoothingFunction().method1
    bleu_score = sentence_bleu(
        [transformed_tokens], original_tokens, smoothing_function=smoothing
    )
    return bleu_score


def extract_docstring_and_content(file_path: str, file_content: Optional[str] = None):
    docstring = ""
    file_content_without_docstring = ""
    if file_content is None:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

    # Extracting docstring using regular expression
    docstring_match = re.search(r"\"\"\"(.+?)\"\"\"", file_content, re.DOTALL)
    docstring = docstring_match.group(1) if docstring_match else None

    # Removing docstring from file content
    file_content_without_docstring = (
        file_content.replace(f'"""{docstring}"""', "") if docstring else file_content
    )

    return docstring, file_content_without_docstring

def generate_bert_docstring(code, model):
    tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
    source_tokens = tokenizer.tokenize(code)[:512-2]
    source_tokens = [tokenizer.cls_token]+source_tokens+[tokenizer.sep_token]
    source_ids =  tokenizer.convert_tokens_to_ids(source_tokens) 
    source_mask = [1] * (len(source_tokens))
    padding_length = 512 - len(source_ids)
    source_ids+=[tokenizer.pad_token_id]*padding_length
    source_mask+=[0]*padding_length
    source_ids = torch.tensor(source_ids).unsqueeze(1)
    source_mask = torch.tensor(source_mask).unsqueeze(1)
    device = torch.device('cpu')
    source_ids.to(device)
    source_mask.to(device)    
    model.eval()
    p = []
    with torch.no_grad():
        preds = model(source_ids=source_ids,source_mask=source_mask)  
        for pred in preds:
            t=pred[0].cpu().numpy()
            t=list(t)
            if 0 in t:
                t=t[:t.index(0)]
            text = tokenizer.decode(t,clean_up_tokenization_spaces=False)
            p.append(text)
    generated_text = p.join()
    return generated_text

if __name__ == "__main__":
    # Example usage
    # method 1
    code = "def addition(a, b): return a + b"
    # doc_string = generate_docstring(code)
    # reference = "this function returns the sum of 2 numbers"
    # fitness = calculate_bleu_score(doc_string, reference)
    # print(f"Fitness: {fitness}")
    model = "roberta/python/checkpoint-best-bleu"

    generate_bert_docstring(code, model)


    # method 2
    # file_path = "./input.py"  # Replace with the actual path to your input.py file
    # reference, code = extract_docstring_and_content(file_path)
    # doc_string = generate_docstring(code)
    # fitness = calculate_bleu_score(doc_string, reference)
    # print(f"Fitness: {fitness}")
