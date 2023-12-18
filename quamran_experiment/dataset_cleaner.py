import csv
import re
import json

def remove_python_comments_and_triple_quotes(text):
    # Remove triple quoted text
    triple_quotes_pattern = r"('''(?:.|\n)*?'''|\"\"\"(?:.|\n)*?\"\"\")"
    text = re.sub(triple_quotes_pattern, '', text, flags=re.DOTALL)

    # Remove single-line comments (e.g., #)
    single_line_comment_pattern = r"#.*?$"
    text = re.sub(single_line_comment_pattern, '', text, flags=re.MULTILINE)

    return text

def process_csv(input_file, output_csv, output_json, code_column_index):
    data = []
    with open(input_file, newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        headers = next(reader)  # Assuming the first row contains headers

        for row in reader:
            if len(row) > code_column_index:
                row[code_column_index] = remove_python_comments_and_triple_quotes(row[code_column_index])
            data.append(row)

    # Write to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)
        writer.writerows(data)

    # Write to JSON
    with open(output_json, 'w', encoding='utf-8') as jsonfile:
        json.dump([dict(zip(headers, row)) for row in data], jsonfile, indent=4)

# Example usage
input_csv = 'dataset_beta.csv'  
output_csv = 'output3.csv'  
output_json = 'output.json' 
code_column_index = 1      
process_csv(input_csv, output_csv, output_json, code_column_index)
