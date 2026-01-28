import pandas as pd
import json
import os
import sys

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'saudipedia-arabic-qa.csv')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'documents.jsonl')

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    # Strip whitespace and collapse multiple spaces
    return " ".join(text.split())

def main():
    print(f"Loading data from: {RAW_DATA_PATH}")
    
    if not os.path.exists(RAW_DATA_PATH):
        print(f"Error: File not found at {RAW_DATA_PATH}")
        sys.exit(1)

    # Robust CSV reading with explicit parameters
    try:
        df = pd.read_csv(
            RAW_DATA_PATH,
            encoding='utf-8',
            sep=',',
            quotechar='"',
            escapechar='\\',
            on_bad_lines='warn',
            dtype=str,  # Read all as string to avoid type inference issues
            keep_default_na=False  # Prevent empty strings from becoming NaN
        )
    except UnicodeDecodeError:
        print("UTF-8 failed, trying utf-8-sig...")
        df = pd.read_csv(
            RAW_DATA_PATH,
            encoding='utf-8-sig',
            sep=',',
            quotechar='"',
            escapechar='\\',
            on_bad_lines='warn',
            dtype=str,
            keep_default_na=False
        )
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    # Validate columns
    required_columns = {'section', 'question', 'answer', 'page_link'}
    if not required_columns.issubset(df.columns):
        print(f"Error: Missing required columns. Found: {df.columns.tolist()}, Expected: {required_columns}")
        sys.exit(1)

    initial_count = len(df)
    print(f"Rows before cleaning: {initial_count}")

    # Drop rows with EMPTY question or answer (not NaN, since we used keep_default_na=False)
    df = df[df['question'].str.strip() != '']
    df = df[df['answer'].str.strip() != '']
    after_dropna_count = len(df)
    print(f"Rows after dropping empty Q/A: {after_dropna_count}")

    # Drop duplicate questions (keep first)
    df = df.drop_duplicates(subset=['question'], keep='first')
    after_dedup_count = len(df)
    print(f"Rows after deduping questions: {after_dedup_count}")

    # Normalize text
    df['question'] = df['question'].apply(normalize_text)
    df['answer'] = df['answer'].apply(normalize_text)

    # Prepare JSONL data
    documents = []
    for index, row in df.iterrows():
        doc = {
            "id": f"{row['section']}_{index}",
            "text": row['answer'],
            "metadata": {
                "question": row['question'],
                "section": row['section'],
                "source": row['page_link']
            }
        }
        documents.append(doc)

    # Write to JSONL
    print(f"Writing {len(documents)} documents to: {PROCESSED_DATA_PATH}")
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    
    with open(PROCESSED_DATA_PATH, 'w', encoding='utf-8') as f:
        for doc in documents:
            json.dump(doc, f, ensure_ascii=False)
            f.write('\n')

    print("Ingestion complete.")

if __name__ == "__main__":
    main()
