import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
INDEX_DIR = os.path.join(DATA_DIR, "faiss_index")

class ASCRO_Retriever:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = None
        self._load_index()
        
    def _load_index(self):
        if os.path.exists(INDEX_DIR):
            self.vectorstore = FAISS.load_local(
                INDEX_DIR, 
                self.embeddings, 
                allow_dangerous_deserialization=True # Local index built by us
            )
        else:
            print("Warning: FAISS index not found. RAG queries will return empty results.")
            
    def search(self, query: str, k: int = 3) -> str:
        """Searches the vector store and returns formatted string of results."""
        if not self.vectorstore:
            return "No RAG knowledge base available."
            
        docs = self.vectorstore.similarity_search(query, k=k)
        
        results = []
        for i, doc in enumerate(docs):
            source = doc.metadata.get('source', 'Unknown source')
            results.append(f"Source: {os.path.basename(source)}\nContent: {doc.page_content}")
            
        return "\n\n---\n\n".join(results)

# Singleton retriever
retriever = ASCRO_Retriever()
