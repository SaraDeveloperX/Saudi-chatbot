
import sys
import os
import weaviate
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from app.rag.retriever import embed_query, COLLECTION_NAME

load_dotenv()

def debug_search(query):
    with open("debug_output.txt", "a", encoding="utf-8") as f:
        f.write(f"--- Debug Search: '{query}' ---\n")
        client = weaviate.connect_to_local(port=8080)
        try:
            query_vector = embed_query(query)
            collection = client.collections.get(COLLECTION_NAME)
            response = collection.query.near_vector(
                near_vector=query_vector,
                limit=1,
                return_metadata=weaviate.classes.query.MetadataQuery(distance=True, certainty=True)
            )
            
            if not response.objects:
                f.write("No results found.\n")
                return

            top = response.objects[0]
            f.write(f"Top Result ID: {top.uuid}\n")
            f.write(f"Metadata: certainty={top.metadata.certainty}, distance={top.metadata.distance}\n")
            f.write(f"Content: {top.properties.get('text', '')[:100]}...\n")

        except Exception as e:
            f.write(f"Error: {e}\n")
        finally:
            client.close()

if __name__ == "__main__":
    # Clear file
    with open("debug_output.txt", "w", encoding="utf-8") as f:
        f.write("")
        
    debug_search("ما عاصمة السعودية؟")
    debug_search("هلا")
    debug_search("ما هي عاصمة فرنسا؟")
