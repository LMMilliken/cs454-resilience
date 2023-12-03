import csv
import openai
import os
from openai import OpenAI
from tqdm import tqdm 

# Set your OpenAI API key
with open("key.txt", "r") as file: 
    api = file.read()
os.environ["OPENAI_API_KEY"] = api

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to generate comment using OpenAI
def generate_comment(code):
    prompt = f"""
    Code: {code}\n\n# You are given to process the Code column and remove all comments from the column and return ONLY the code. 
    Your answer should be in this format: {{"Code": "your written code"}}.\n"""
    response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": f""}
    ])
    return response.choices[0].message.content

# Path to your CSV file
csv_file_path = 'converted_500.csv'
output_file_path = 'only_code3.csv'  # Output file name

# Process the CSV file and write to a new CSV file
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file, open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
    reader = csv.DictReader(csv_file)
    fieldnames = ['code', 'docstring', 'only_code']  # Specify the desired output columns
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    
    writer.writeheader()

    # Process only the first 100 rows
    for i, row in tqdm(enumerate(reader), desc="Processing Rows", unit="row"):
        if i >= 100:  # Stop after processing 100 rows
            break
        code = generate_comment(row['code'])
        # Write only the specified columns to the new file
        writer.writerow({'code': row['code'], 'docstring': row['docstring'], 'only_code': code})
        print(code)

print(f"Completed processing the first 100 rows. Output written to {output_file_path}.")
