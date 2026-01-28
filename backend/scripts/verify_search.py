import weaviate
import os
import sys
import numpy as np
from dotenv import load_dotenv

ST_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBEDDING_PROVIDER = None

def get_embedding_model():
    global EMBEDDING_PROVIDER
    
    # Provider 1: Sentence Transformers (Try first)
    # print(f"Attempting to load local model: {ST_MODEL_NAME}...")
    # try:
    #     from sentence_transformers import SentenceTransformer
    #     model = SentenceTransformer(ST_MODEL_NAME)
    #     print("Local model loaded.")
    #     EMBEDDING_PROVIDER = "ST"
    #     return model
    # except Exception as e:
    #     print(f"Local model failed: {e}")
    #     print("Falling back to OpenAI...")
    pass

    # Provider 2: OpenAI
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY missing.")
        sys.exit(1)
        
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        EMBEDDING_PROVIDER = "OPENAI"
        return client
    except Exception as e:
        print(f"OpenAI Init Error: {e}")
        sys.exit(1)

def encode_text(model, text):
    if EMBEDDING_PROVIDER == "ST":
        return model.encode(text).astype(np.float32).tolist()
    elif EMBEDDING_PROVIDER == "OPENAI":
        text = text.replace("\n", " ")
        return model.embeddings.create(input=[text], model="text-embedding-3-small").data[0].embedding

def main():
    print("Connecting to Weaviate at http://localhost:8080...")
    client = weaviate.connect_to_local(port=8080)
    
    collection_name = "KnowledgeDocument"
    model = get_embedding_model()
    
    queries = [
        "متى تأسست المملكة العربية السعودية؟",
        "من هو الملك عبد العزيز؟"
    ]
    
    for q in queries:
        print(f"\nQuery: {q}")
        vec = encode_text(model, q)
        
        response = client.collections.get(collection_name).query.near_vector(
            near_vector=vec,
            limit=5,
            return_metadata=weaviate.classes.query.MetadataQuery(distance=True, score=True)
        )

        for i, obj in enumerate(response.objects):
            print(f"Result {i+1} (Score: {obj.metadata.distance:.4f}):")
            print(f"Section: {obj.properties.get('section')}")
            print(f"Source: {obj.properties.get('source')}")
            print(f"Snippet: {obj.properties.get('text')[:100]}...")

    client.close()

if __name__ == "__main__":
    main()
