from transformers import AutoTokenizer
from collections import Counter
from tqdm.auto import tqdm 

def count_unique_tokens(file_path, model_name, chunk_size=512, top_n=30):
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    token_counts = Counter()

    with open(file_path, 'r', encoding='utf-8') as file:
        file_size = sum(1 for _ in file)  # Count lines for progress bar
        file.seek(0)  # Reset file pointer

        with tqdm(total=file_size, desc="Tokenizing") as pbar:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                # Tokenize and update counts
                tokens = tokenizer.tokenize(chunk)
                token_counts.update(tokens)
                pbar.update(len(chunk.splitlines()))  # Update progress based on lines read

    return token_counts.most_common(top_n)

def main():
    input_txt_file = "C:\\Python\\new folder\\Assignment 2\\text.txt"
    model_name = 'bert-base-uncased'
    top_tokens = count_unique_tokens(input_txt_file, model_name)

    print('Top 30 unique tokens and their counts:')
    for token, count in top_tokens:
        print(f'{token}: {count}')

if __name__ == "__main__":
    main()
