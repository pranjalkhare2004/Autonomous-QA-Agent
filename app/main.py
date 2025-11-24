from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.ingestion import ingest_file, clear_knowledge_base
from app.services.rag_service import retrieve_context

app = FastAPI(title="QA Agent API")

class TestGenRequest(BaseModel):
    query: str

class SeleniumGenRequest(BaseModel):
    test_case: dict
    html_content: str

@app.get("/")
def read_root():
    return {"message": "QA Agent API is running"}

@app.post("/ingest/")
async def ingest_documents(files: List[UploadFile] = File(...)):
    total_chunks = 0
    processed_files = []
    
    for file in files:
        content = await file.read()
        try:
            chunks = ingest_file(file.filename, content)
            total_chunks += chunks
            processed_files.append(file.filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing {file.filename}: {str(e)}")
            
    return {"message": "Ingestion successful", "files": processed_files, "total_chunks": total_chunks}

@app.post("/clear-kb/")
def clear_kb():
    clear_knowledge_base()
    return {"message": "Knowledge base cleared"}

@app.post("/retrieve/")
def retrieve(request: TestGenRequest):
    context = retrieve_context(request.query)
    return {"context": context}

# Placeholder endpoints for Phase 2 & 3
from app.services.llm_service import generate_test_cases

@app.post("/generate-tests/")
def generate_tests(request: TestGenRequest):
    context = retrieve_context(request.query)
    if not context:
        raise HTTPException(status_code=404, detail="No relevant context found in knowledge base.")
        
    test_cases = generate_test_cases(context, request.query)
    return {"test_cases": test_cases}

from app.services.llm_service import generate_selenium_script

@app.post("/generate-selenium/")
def generate_selenium(request: SeleniumGenRequest):
    script = generate_selenium_script(request.test_case, request.html_content)
    return {"selenium_script": script}
