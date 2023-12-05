import  os
from openai import OpenAI
from nltk.translate.bleu_score import sentence_bleu

with open("key.txt", "r") as file: 
    api = file.read()
os.environ["OPENAI_API_KEY"] = api
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_docstring(code):
    prompt = f"""Code: {code}\n\n# You are given a python code. Your task is to go through the code and generate natural language comments explaining what the code does. Think of it as writing a docstring for the code. However try to keep them short and concise and try to give the overall idea of the function does. Also avoid using the function name. Start like this: This function ........\n"""
    
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": f""}
      ]
    )
    return response.choices[0].message.content

def calculate_bleu_score(predictions,references):
    original_tokens = predictions.split()
    transformed_tokens = references.split()
    bleu_score = sentence_bleu([original_tokens], transformed_tokens)
    return bleu_score

if __name__ == "__main__":
    resp = "def add(a, b): return a + b"
    references = "def addition(a, b): return a + b"

    fitness = calculate_bleu_score(resp, references)

    print(f"Fitness: {fitness}")