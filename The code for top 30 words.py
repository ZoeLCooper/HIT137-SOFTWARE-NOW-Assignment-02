import csv
import sys
from collections import Counter
import re

def get_top_words(file_path, top_n=30, chunk_size=1024):
    word_counts = Counter()

    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            words = re.findall(r'\b(?![0-9]+\b)\w+\b', chunk.lower()) 
            word_counts.update(words)

    return word_counts.most_common(top_n)

def write_top_words_to_csv(top_words, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Word', 'Count'])
        writer.writerows(top_words)

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_txt_file> <output_csv_file>")
        return

    input_txt_file = sys.argv[1]
    output_csv_file = sys.argv[2]

    try:
        top_words = get_top_words(input_txt_file)
        write_top_words_to_csv(top_words, output_csv_file)
        print(f'Top 30 words and their counts saved to {output_csv_file}')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
