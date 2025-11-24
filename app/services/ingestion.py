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

# Persistent Directory for ChromaDB
PERSIST_DIRECTORY = "./chroma_db"

def get_vector_store():
    if os.path.exists(PERSIST_DIRECTORY):
        return Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
    return Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)

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
    vector_store.persist()
    
    return len(documents)

def clear_knowledge_base():
    if os.path.exists(PERSIST_DIRECTORY):
        import shutil
        shutil.rmtree(PERSIST_DIRECTORY)
