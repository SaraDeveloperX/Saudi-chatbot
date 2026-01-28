import weaviate
from weaviate.classes.config import Property, DataType, Configure
import sys

def main():
    print("Connecting to Weaviate at http://localhost:8080...")
    
    try:
        # Connect to localized Weaviate
        client = weaviate.connect_to_local(port=8080)
        
    except Exception as e:
        # Graceful exit if Weaviate is not available
        print(f"Weaviate not available, schema creation skipped. Error: {e}")
        sys.exit(0)

    try:
        if not client.is_ready():
            print("Weaviate is not ready, schema creation skipped.")
            sys.exit(0)

        collection_name = "KnowledgeDocument"
        
        if client.collections.exists(collection_name):
            print(f"Collection '{collection_name}' already exists.")
        else:
            print(f"Creating collection '{collection_name}'...")
            client.collections.create(
                name=collection_name,
                properties=[
                    Property(name="text", data_type=DataType.TEXT),
                    Property(name="question", data_type=DataType.TEXT),
                    Property(name="section", data_type=DataType.TEXT, skip_vectorization=True),
                    Property(name="source", data_type=DataType.TEXT, skip_vectorization=True),
                ],
                # Basic configuration - no specific vectorizer set (will rely on default or none as per docker-compose)
            )
            print(f"Collection '{collection_name}' created successfully.")

    except Exception as e:
        print(f"An error occurred during schema operations: {e}")
        # Even if error in logic, we strictly follow the requirement:
        # "If Weaviate is unreachable... exit with code 0". 
        # But if it was reachable and failed later, we might want to know.
        # However, the user said "If Weaviate is unreachable...".
        # If client was created, it was reachable. 
        # I will let this print error but exit 1 if it's a logic error, 
        # but connection error handled above.
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    main()
