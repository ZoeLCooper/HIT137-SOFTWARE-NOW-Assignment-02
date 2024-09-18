import spacy
from transformers import AutoModelForTokenClassification, AutoTokenizer
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter 

# Load models
nlp_sci = spacy.load("en_core_sci_sm")
nlp_bc5 = spacy.load("en_ner_bc5cdr_md")
tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-v1.1")
model = AutoModelForTokenClassification.from_pretrained("dmis-lab/biobert-v1.1")

# Set max_length for models
nlp_sci.max_length = 10**9
nlp_bc5.max_length = 10**9

def extract_entities(text, model_name):
    try:
        doc = nlp_sci(text) if model_name == "scispaCy" else nlp_bc5(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ("DISEASE", "CHEMICAL")]
        return entities
    except Exception as e:
        print(f"Error extracting entities with {model_name}: {e}")
        return []

def compare_entities(entities1, entities2):
    set_sci = set(entities1)
    set_biobert = set(entities2)

    common = set_sci & set_biobert
    unique_sci = set_sci - set_biobert
    unique_biobert = set_biobert - set_sci

    return (
        len(entities1), 
        len(entities2), 
        common, 
        unique_sci, 
        unique_biobert, 
        get_common_words(entities1), 
        get_common_words(entities2)
    )

def get_common_words(entities):
    all_words = [word.lower() for entity, _ in entities for word in entity.split()]
    return Counter(all_words).most_common(10)

def process_chunk(chunk):
    entities_sci = extract_entities(chunk, "scispaCy")
    entities_biobert = extract_entities(chunk, "BioBERT")
    return compare_entities(entities_sci, entities_biobert)

# Read text from file
try:
    with open("C:\\Python\\new folder\\Assignment 2\\text.txt", "r", encoding="utf-8") as f:
        text = f.read()
except Exception as e:
    print(f"Error reading the file: {e}")
    text = ""

print("Processing text...")
start_time = time.time()

chunks = text.split(".")
num_chunks = len(chunks)
batch_size = 10 

with ThreadPoolExecutor() as executor:
    futures = []
    for i in range(0, num_chunks, batch_size):
        batch = chunks[i:i + batch_size]
        future = executor.submit(process_chunk, ".".join(batch))
        futures.append(future)

    for completed_count, future in enumerate(as_completed(futures), start=1):
        result_tuple = future.result()
        total_sci, total_biobert, common, unique_sci, unique_biobert, common_words_sci, common_words_biobert = result_tuple

        print(f"\n**Comparison of entities for batch {completed_count}:**")
        print(f"Total entities detected by scispaCy: {total_sci}")
        print(f"Total entities detected by BioBERT: {total_biobert}")
        print(f"Common entities: {common}")
        print(f"Unique entities in scispaCy: {unique_sci}")
        print(f"Unique entities in BioBERT: {unique_biobert}")
        print(f"Most common words in scispaCy entities: {common_words_sci}")
        print(f"Most common words in BioBERT entities: {common_words_biobert}")

        progress_percentage = (completed_count / len(futures)) * 100
        print(f"\rProcessed batches {completed_count}/{len(futures)} ({progress_percentage:.2f}%)", end="")

print(f"\nProcessing completed in {time.time() - start_time:.2f} seconds.")
