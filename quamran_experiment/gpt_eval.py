import csv
import openai
import os
from openai import OpenAI
from tqdm import tqdm

# Set your OpenAI API key
with open("../key.txt", "r") as file:
    api = file.read()
os.environ["OPENAI_API_KEY"] = api


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Function to generate comment using OpenAI
def generate_comment(code):
    prompt = f"""Code: {code}\n\n# You are given a python code. Your task is to go through the code and 
    generate natural language comments explaining what the code does.
    Think of it as writing a docstring for the code. Also avoid using the function name. 
    Instead of explaining in details, just provide a high level idea.
    Make sure to keep the responses within 30 words (THIS IS MANDATORY). Start like this:
    This function ........\n"""
    
    response = client.chat.completions.create(
    model="gpt-3.5-turbo", #gpt-4-1106-preview
    messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": f""}
      ]
    )
    return response.choices[0].message.content


# Path to your CSV file
# Path to your CSV file
csv_file_path = 'dataset.csv'
output_file_path = 'output_with_comments_GPT3.5_(30 words).csv'  # Output file name

# Process the CSV file and write to a new CSV file
with open(csv_file_path, mode="r", newline="", encoding="utf-8") as csv_file, open(
    output_file_path, mode="w", newline="", encoding="utf-8"
) as output_file:
    reader = csv.DictReader(csv_file)
    fieldnames = reader.fieldnames + [
        "generated_comment"
    ]  # Add a new field for comments
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)

    writer.writeheader()
    for row in tqdm(reader):
        comment = generate_comment(row["code"])
        row["generated_comment"] = comment
        writer.writerow(row)
        print(row["generated_comment"])

print(f"Completed processing the CSV file. Output written to {output_file_path}.")
