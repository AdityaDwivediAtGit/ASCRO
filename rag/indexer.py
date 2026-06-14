import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DOCS_DIR = os.path.join(DATA_DIR, "docs")
INDEX_DIR = os.path.join(DATA_DIR, "faiss_index")

def build_index():
    print(f"Loading documents from {DOCS_DIR}...")
    loader = DirectoryLoader(DOCS_DIR, glob="*.md", loader_cls=TextLoader)
    docs = loader.load()
    
    if not docs:
        print("No documents found. Please run generate_synthetic_data.py first.")
        return
        
    print(f"Loaded {len(docs)} documents. Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    
    print("Generating embeddings (using sentence-transformers/all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Building FAISS index...")
    vectorstore = FAISS.from_documents(splits, embeddings)
    
    os.makedirs(INDEX_DIR, exist_ok=True)
    vectorstore.save_local(INDEX_DIR)
    print(f"FAISS index saved to {INDEX_DIR}")

if __name__ == "__main__":
    build_index()
