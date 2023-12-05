import  os
from openai import OpenAI
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

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

def calculate_bleu_score(predictions, references):
    original_tokens = predictions.split()
    transformed_tokens = references.split()

    smoothing = SmoothingFunction().method1
    bleu_score = sentence_bleu([transformed_tokens], original_tokens, smoothing_function=smoothing)
    
    return bleu_score

if __name__ == "__main__":
    code = "def addition(a, b): return a + b"
    doc_string = generate_docstring(code)
    reference = "this function returns the sum of 2 numbers"

    fitness = calculate_bleu_score(doc_string, reference)

    print(f"Fitness: {fitness}")