import weaviate
import sys

def main():
    print("Connecting to Weaviate at http://localhost:8080...")
    client = weaviate.connect_to_local(port=8080)
    
    collection_name = "KnowledgeDocument"
    
    if client.collections.exists(collection_name):
        print(f"Deleting collection '{collection_name}'...")
        client.collections.delete(collection_name)
        print("Collection deleted.")
    else:
        print(f"Collection '{collection_name}' does not exist.")

    client.close()

if __name__ == "__main__":
    main()
