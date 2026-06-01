import os
import re
import chromadb

def clean_text(text):
    """
    Cleans raw student documents by stripping out boilerplate artifacts,
    HTML remnants, and repetitive structural noise.
    """
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&amp;', '&').replace('&nbsp;', ' ').replace('&#39;', "'")
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def chunk_document(text, source_name, chunk_size=400, overlap=100):
    """
    Splits text cleanly using a precise window size and overlapping strategy.
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    if text_length <= chunk_size:
        return [{"text": text, "metadata": {"source": source_name, "position": 0}}]
        
    while start < text_length:
        end = start + chunk_size
        chunk_text = text[start:end]
        
        chunks.append({
            "text": chunk_text,
            "metadata": {
                "source": source_name,
                "position": start
            }
        })
        start += (chunk_size - overlap)
        
    return chunks

def run_pipeline():
    docs_dir = "documents"
    all_chunks = []
    
    if not os.path.exists(docs_dir):
        print(f"❌ Error: The '{docs_dir}' directory does not exist yet.")
        return
        
    print("🚀 Ingestion Pipeline Started...")
    
    for filename in os.listdir(docs_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(docs_dir, filename)
            
            with open(file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()
                
            cleaned_content = clean_text(raw_content)
            file_chunks = chunk_document(cleaned_content, filename)
            all_chunks.extend(file_chunks)
            
            print(f"📂 Processed {filename} -> Generated {len(file_chunks)} chunks.")

    print(f"\n✅ Ingestion Complete! Total chunks extracted: {len(all_chunks)}")
    
    # --- CHROMADB INTEGRATION ---
    if all_chunks:
        print("\n📦 Initializing Local ChromaDB Vector Database...")
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        collection = chroma_client.get_or_create_collection(name="ucsd_guide_collection")
        
        print("📥 Upserting chunks into vector database...")
        
        # Prepare arrays for batch insertion
        documents = [chunk["text"] for chunk in all_chunks]
        metadatas = [chunk["metadata"] for chunk in all_chunks]
        ids = [f"{chunk['metadata']['source']}_chunk_{chunk['metadata']['position']}" for chunk in all_chunks]
        
        # Using .upsert() ensures old empty file records get completely overwritten
        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"🔒 Successfully indexed/updated {collection.count()} chunks into 'ucsd_guide_collection'!")
        
    return all_chunks

if __name__ == "__main__":
    run_pipeline()