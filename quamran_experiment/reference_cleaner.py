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
def generate_comment(info):
    prompt = f"""Information: {info}\n\n# You are given some information in string format. Your task is to go through them and remove some part of it
    and return the rest of the string. You have to remove the stuff like :type, :param, :return, :rtype etc. and return the rest of the string.
    You can also remove the newlines any extra spaces.\n"""
    
    response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": f""}
      ]
    )
    return response.choices[0].message.content

# Path to your CSV file
# Path to your CSV file
csv_file_path = 'reference_cleaned.csv'
output_file_path = 'reference_cleaned_gpt4.csv'  # Output file name

# Process the CSV file and write to a new CSV file
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file, open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
    reader = csv.DictReader(csv_file)
    fieldnames = reader.fieldnames + ['stuff']  # Add a new field for comments
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in tqdm(reader):
        comment = generate_comment( row['string'])
        row['stuff'] = comment
        writer.writerow(row)
        print(row['stuff'])

print(f"Completed processing the CSV file. Output written to {output_file_path}.")

