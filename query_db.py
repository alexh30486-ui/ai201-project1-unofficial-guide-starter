import chromadb

def search_campus_guide(query_text, n_results=1):
    # Connect to the exact same persistent directory
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    # Get our existing collection
    collection = chroma_client.get_collection(name="ucsd_guide_collection")
    
    print(f"🔍 Searching for: \"{query_text}\"\n")
    
    # Query the collection
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    # Print the matching results nicely
    for i in range(len(results['documents'][0])):
        print(f"📍 Match #{i+1}")
        print(f"Source Document: {results['metadatas'][0][i]['source']}")
        print(f"Distance Score: {results['distances'][0][i]:.4f}")
        print(f"Content:\n\"{results['documents'][0][i]}\"")
        print("-" * 40)

if __name__ == "__main__":
    # Test your vector search with a specific question!
    search_campus_guide("Where is a quiet place to study for exams?")