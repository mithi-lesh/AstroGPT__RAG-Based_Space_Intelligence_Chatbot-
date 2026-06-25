from fastapi import FastAPI, UploadFile, Form, File
from pydantic import BaseModel
from typing import List, Dict

class ChatRequest(BaseModel):
    query: str
    history: List[Dict[str, str]] = []
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import rag_engine

app = FastAPI(title="Astro-GPT Backend API")

# Setup CORS to allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF document to be chunked and added to the Chroma vector database."""
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        num_chunks = rag_engine.process_document(temp_path, file.filename)
        return {"status": "success", "chunks": num_chunks, "filename": file.filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/query")
async def query_astro(request: ChatRequest):
    """Query Astro-GPT with contextual conversation memory."""
    try:
        response_text, context_chunks = rag_engine.query_astro_gpt(request.query, request.history)
        return {
            "status": "success", 
            "response": response_text, 
            "context": context_chunks
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
