import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'saudipedia-arabic-qa.csv')

def main():
    print(f"Inspecting: {RAW_DATA_PATH}")
    print(f"File size: {os.path.getsize(RAW_DATA_PATH)} bytes")
    
    # Try multiple encodings
    for encoding in ['utf-8', 'utf-8-sig', 'latin-1']:
        try:
            df = pd.read_csv(
                RAW_DATA_PATH,
                encoding=encoding,
                sep=',',
                quotechar='"',
                on_bad_lines='warn'
            )
            print(f"\nEncoding: {encoding} - SUCCESS")
            break
        except Exception as e:
            print(f"Encoding {encoding} failed: {e}")
            continue
    else:
        print("All encodings failed.")
        return

    print(f"\nRow count: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    
    print("\nNon-null counts:")
    for col in ['section', 'question', 'answer', 'page_link']:
        if col in df.columns:
            print(f"  {col}: {df[col].notna().sum()}")
        else:
            print(f"  {col}: MISSING COLUMN")

    print("\nSample rows (Q/A lengths):")
    for i, row in df.head(5).iterrows():
        q_len = len(str(row.get('question', '')))
        a_len = len(str(row.get('answer', '')))
        print(f"  Row {i}: Q={q_len} chars, A={a_len} chars")

if __name__ == "__main__":
    main()
