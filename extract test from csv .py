import csv
import os

def extract_text_from_csv(csv_file_path, column_name='TEXT'):
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            text_column = [row[column_name] for row in reader if column_name in row]
        return text_column
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
        return []
    except Exception as e:
        print(f"Error reading {csv_file_path}: {e}")
        return []

def write_to_txt(output_file_path, text_list):
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            for text in text_list:
                file.write(text + '\n')
        print(f'Text written to {output_file_path}')
    except Exception as e:
        print(f"Error writing to {output_file_path}: {e}")

def extract_and_merge_csv_files(csv_folder_path, output_txt_file, column_name='TEXT'):
    all_text = []

    if not os.path.isdir(csv_folder_path):
        print(f"Directory not found: {csv_folder_path}")
        return

    for filename in os.listdir(csv_folder_path):
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(csv_folder_path, filename)
            text_column = extract_text_from_csv(csv_file_path, column_name)
            all_text.extend(text_column)

    write_to_txt(output_txt_file, all_text)

# Usage
csv_folder = "C:\\Python\\new folder\\Assignment 2"
output_txt_file = 'text.txt'

extract_and_merge_csv_files(csv_folder, output_txt_file)
