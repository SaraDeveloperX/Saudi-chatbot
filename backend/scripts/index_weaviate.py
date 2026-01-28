import json
import os
import sys
import weaviate
import numpy as np
from weaviate.util import generate_uuid5
from weaviate.classes.data import DataObject
from dotenv import load_dotenv

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'documents.jsonl')
CHECKPOINT_PATH = os.path.join(BASE_DIR, 'storage', 'weaviate_indexed_ids.txt')

# Configuration
BATCH_SIZE = 64
COLLECTION_NAME = "KnowledgeDocument"
ST_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Global provider tracker
EMBEDDING_PROVIDER = None # "ST" or "OPENAI"

def load_checkpoint():
    if not os.path.exists(CHECKPOINT_PATH):
        return set()
    with open(CHECKPOINT_PATH, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def update_checkpoint(ids):
    os.makedirs(os.path.dirname(CHECKPOINT_PATH), exist_ok=True)
    with open(CHECKPOINT_PATH, 'a', encoding='utf-8') as f:
        for doc_id in ids:
            f.write(f"{doc_id}\n")

def get_embedding_model():
    global EMBEDDING_PROVIDER
    
    # Provider 1: Sentence Transformers (Local)
    try:
        raise Exception("Forcing fallback to OpenAI due to slow download")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(ST_MODEL_NAME)
        print("Local model loaded successfully.")
        EMBEDDING_PROVIDER = "ST"
        return model
    except Exception as e:
        print(f"Failed to load local model: {e}")
        print("Falling back to Provider 2: OpenAI...")

    # Provider 2: OpenAI (API)
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment. Cannot use fallback provider.")
        sys.exit(1)
        
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        print("OpenAI client initialized.")
        EMBEDDING_PROVIDER = "OPENAI"
        return client
    except Exception as e:
        print(f"Failed to initialize OpenAI client: {e}")
        sys.exit(1)

def encode_text(model, texts):
    if EMBEDDING_PROVIDER == "ST":
        # Check if vector is float32
        return model.encode(texts).astype(np.float32)
    elif EMBEDDING_PROVIDER == "OPENAI":
        # Batching for OpenAI is handled here or by caller. 
        # Caller does batching (BATCH_SIZE=64 is fine for OpenAI).
        # OpenAI text-embedding-3-small
        try:
            # Replace newlines
            clean_texts = [t.replace("\n", " ") for t in texts]
            response = model.embeddings.create(input=clean_texts, model="text-embedding-3-small")
            return [data.embedding for data in response.data]
        except Exception as e:
            print(f"OpenAI Embedding Error: {e}")
            raise e
    else:
        raise ValueError("Unknown embedding provider")

def main():
    print(f"Connecting to Weaviate at http://localhost:8080...")
    client = weaviate.connect_to_local(port=8080)
    
    if not client.is_ready():
        print("Error: Weaviate is not ready.")
        sys.exit(1)
    
    # Initialize Embedding Model
    model = get_embedding_model()

    print(f"Loading documents from {PROCESSED_DATA_PATH}")
    if not os.path.exists(PROCESSED_DATA_PATH):
        print("Error: documents.jsonl not found.")
        sys.exit(1)

    with open(PROCESSED_DATA_PATH, 'r', encoding='utf-8') as f:
        documents = [json.loads(line) for line in f]

    print(f"Total documents: {len(documents)}")

    indexed_ids = load_checkpoint()
    print(f"Already indexed: {len(indexed_ids)}")

    docs_to_index = [doc for doc in documents if doc['id'] not in indexed_ids]
    print(f"Documents to index: {len(docs_to_index)}")

    if not docs_to_index:
        print("All documents already indexed.")
    else:
        collection = client.collections.get(COLLECTION_NAME)
        
        # Batch processing
        total_batches = (len(docs_to_index) + BATCH_SIZE - 1) // BATCH_SIZE
        
        for i in range(0, len(docs_to_index), BATCH_SIZE):
            print(f"Starting batch {i}", flush=True)
            batch_docs = docs_to_index[i:i + BATCH_SIZE]
            batch_texts = [doc['text'] for doc in batch_docs] 
            
            try:
                # Generate embeddings
                # print("Encoding...", flush=True)
                embeddings = encode_text(model, batch_texts)
                
                # Prepare objects for Weaviate
                objects_to_insert = []
                current_ids = []
                
                for j, doc in enumerate(batch_docs):
                    properties = {
                        "text": doc['text'],
                        "question": doc['metadata']['question'],
                        "section": doc['metadata']['section'],
                        "source": doc['metadata']['source'],
                    }
                    
                    vector = embeddings[j]
                    if isinstance(vector, np.ndarray):
                        vector = vector.tolist()

                    objects_to_insert.append(DataObject(
                        properties=properties,
                        vector=vector,
                    ))
                    current_ids.append(doc['id'])
                
                # Insert batch
                # print("Inserting...", flush=True)
                result = collection.data.insert_many(objects_to_insert)
                if result.has_errors:
                     print(f"Errors in batch {i}: {result.errors}", file=sys.stdout, flush=True)
                
                # Update checkpoint
                update_checkpoint(current_ids)
                
                if (i // BATCH_SIZE + 1) % 5 == 0 or (i + BATCH_SIZE >= len(docs_to_index)):
                     print(f"Indexed batch {i // BATCH_SIZE + 1}/{total_batches} ({len(batch_docs)} docs) - {EMBEDDING_PROVIDER}", flush=True)

            except Exception as e:
                print(f"BATCH_ERROR: {str(e)[:200]}", file=sys.stdout, flush=True)
                break

    # Final Verification COUNT
    agg = client.collections.get(COLLECTION_NAME).aggregate.over_all(total_count=True)
    print(f"Total objects in Weaviate '{COLLECTION_NAME}': {agg.total_count}")
    client.close()

if __name__ == "__main__":
    main()
