import csv
import openai
import  os
from openai import OpenAI
from tqdm import tqdm

# Set your OpenAI API key
with open("key.txt", "r") as file: 
    api = file.read()
os.environ["OPENAI_API_KEY"] = api


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to generate comment using OpenAI
def generate_comment(code):
    prompt = f"""Code: {code}\n\n# You are given a python code. Your task is to go through the code and generate natural language comments explaining what the code does. 
    Think of it as writing a docstring for the code. However try to keep them short and concise and
    try to give the overall idea of the function does. Also avoid using the function name. Start like this:
    This function ........\n"""
    
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": f""}
      ]
    )
    return response.choices[0].message.content

# Path to your CSV file
# Path to your CSV file
csv_file_path = 'dataset.csv'
output_file_path = 'output_with_comments_GPT3.5_v2.csv'  # Output file name

# Process the CSV file and write to a new CSV file
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file, open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
    reader = csv.DictReader(csv_file)
    fieldnames = reader.fieldnames + ['generated_comment']  # Add a new field for comments
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in tqdm(reader):
        comment = generate_comment( row['code'])
        row['generated_comment'] = comment
        writer.writerow(row)
        print(row['generated_comment'])

print(f"Completed processing the CSV file. Output written to {output_file_path}.")

