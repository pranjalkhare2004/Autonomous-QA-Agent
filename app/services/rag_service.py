from app.services.ingestion import get_vector_store

def retrieve_context(query: str, k: int = 3) -> str:
    vector_store = get_vector_store()
    docs = vector_store.similarity_search(query, k=k)
    
    context = ""
    for doc in docs:
        context += f"Source: {doc.metadata['source']}\nContent: {doc.page_content}\n\n"
    
    return context
