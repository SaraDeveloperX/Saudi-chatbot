
import weaviate
import os
import json

def debug_search():
    try:
        # Use v4 connect helper
        client = weaviate.connect_to_local(port=8080)
        
        try:
            query = "ما عاصمة السعودية؟"
            
            # Use collections API
            collection = client.collections.get("KnowledgeDocument") # Updated from SaudipediaChunk based on retriever.py
            
            # Simple vector search - we need an embedding first or use near_text if configured
            # But let's check retriever.py - it uses near_vector with OpenAI embedding.
            # To simplify debug, let's just use near_text if 'vectorizer' is set in schema, 
            # OR honestly just re-use retriever.retrieve logic but printed out.
            # Actually, retriever.py is already right there. Let's just import and use it!
            
            import sys
            sys.path.append(os.getcwd())
            from app.rag.retriever import retrieve, embed_query
            
            # Let's manual call to inspect metadata
            query_vector = embed_query(query)
            response = collection.query.near_vector(
                near_vector=query_vector,
                limit=1,
                return_metadata=weaviate.classes.query.MetadataQuery(distance=True, certainty=True)
            )
            
            for obj in response.objects:
                print(f"Distance: {obj.metadata.distance}")
                print(f"Certainty: {obj.metadata.certainty}")
                
        finally:
            client.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_search()
