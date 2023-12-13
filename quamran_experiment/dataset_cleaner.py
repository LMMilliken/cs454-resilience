import csv
import re

def remove_python_comments_and_triple_quotes(text):
    # Remove triple quoted text
    triple_quotes_pattern = r"('''(?:.|\n)*?'''|\"\"\"(?:.|\n)*?\"\"\")"
    text = re.sub(triple_quotes_pattern, '', text, flags=re.DOTALL)

    # Remove single-line comments (e.g., #)
    single_line_comment_pattern = r"#.*?$"
    text = re.sub(single_line_comment_pattern, '', text, flags=re.MULTILINE)

    return text

def process_csv(input_file, output_file, code_column_index):
    with open(input_file, newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            if len(row) > code_column_index:
                row[code_column_index] = remove_python_comments_and_triple_quotes(row[code_column_index])
            writer.writerow(row)

# Example usage
input_csv = 'dataset_beta.csv'  # Replace with your input file name
output_csv = 'output2.csv' # Replace with your desired output file name
code_column_index = 1     # Replace with the index of the "code" column
process_csv(input_csv, output_csv, code_column_index)
