import os
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from app.utils.parsers import parse_file

# Initialize Embeddings
# Note: Ensure GOOGLE_API_KEY is set in environment variables
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Global in-memory vector store for cloud deployment
_vector_store = None

def get_vector_store():
    """
    Get or create an in-memory ChromaDB instance.
    This approach works with cloud platforms that don't support persistent storage.
    """
    global _vector_store
    if _vector_store is None:
        # Create in-memory ChromaDB (no persist_directory = in-memory)
        _vector_store = Chroma(embedding_function=embeddings)
    return _vector_store

def ingest_file(filename: str, content: bytes):
    text_content = parse_file(filename, content)
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text_content)
    
    # Create Documents with metadata
    documents = [
        Document(page_content=chunk, metadata={"source": filename})
        for chunk in chunks
    ]
    
    # Add to Vector Store
    vector_store = get_vector_store()
    vector_store.add_documents(documents)
    
    return len(documents)

def clear_knowledge_base():
    """
    Clear the in-memory knowledge base by resetting the global vector store.
    """
    global _vector_store
    _vector_store = None
