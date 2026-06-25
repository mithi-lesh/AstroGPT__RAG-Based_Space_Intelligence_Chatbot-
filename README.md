# Astro-GPT: Astronomical Interpreter

A space-themed Retrieval-Augmented Generation (RAG) project that ingests PDF and text documents, stores domain knowledge in a local ChromaDB vector database, and answers astrophysics questions using Google Gemini.

## Overview

This repository contains a small-language-model assistant for astronomy research and astrophysics interpretation. The system can:
- ingest PDF documents and other supported files
- chunk and embed text into a local ChromaDB collection
- perform semantic search using SentenceTransformers
- synthesize answers using the Google Gemini API
- fallback to NASA Image and Video Library search when local context is missing

## Key Components

- `app.py` - Streamlit frontend for file upload, API key input, and chat interaction
- `main.py` - FastAPI backend exposing `/upload` and `/query` endpoints
- `rag_engine.py` - Document processing, vector storage, semantic retrieval, and Gemini API integration
- `requirements.txt` - Python dependencies for the core project
- `chroma_db/` - Local ChromaDB persistence folder
- `frontend/` - React/Vite starter app scaffolded separately

## Features

- PDF ingestion and text extraction
- CSV, PPTX/PPT, and TXT processing support
- Text chunking with overlap for better semantic retrieval
- Local vector search via ChromaDB
- Google Gemini `gemini-2.5-flash` response generation
- NASA API fallback when local vector context is insufficient

## Requirements

- Python 3.10+ (recommended)
- `venv` or equivalent virtual environment
- `requirements.txt` dependencies
- Google Gemini API key

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file if needed and set your Gemini API key there or provide it at runtime in the Streamlit sidebar.

Example `.env` content:

```text
gemini_api=YOUR_GEMINI_API_KEY
```

## Running the Project

### Option 1: Run the Streamlit app directly

```powershell
python app.py
```

Then open the local Streamlit URL in your browser.

### Option 2: Run the FastAPI backend

```powershell
uvicorn main:app --reload
```

The backend exposes:
- `POST /upload` for document ingestion
- `POST /query` for chat queries

## Usage

1. Start the app or backend.
2. Add your Google Gemini API key.
3. Upload astronomy-related PDFs via the sidebar.
4. Ask astrophysics questions in the chat input.
5. Review retrieved document context in the expandable section.

## Notes

- The project uses a local `chroma_db` folder to persist embeddings and documents.
- If no local context is found, the system tries a NASA public search fallback.
- The `frontend/` directory contains a separate React/Vite project template and is not required for the current Streamlit-based app.

## Project Structure

- `app.py` - Streamlit UI
- `main.py` - FastAPI backend
- `rag_engine.py` - RAG pipeline implementation
- `requirements.txt` - Python requirements
- `chroma_db/` - persisted ChromaDB files
- `frontend/` - React/Vite frontend scaffold
- `project_report.md` - project report documentation
- `project_report_summary.txt` - summary of another project component

## Troubleshooting

- Ensure the Google Gemini API key is valid and accessible via `os.environ["gemini_api"]` or `.env`.
- Confirm `chroma_db` is writable and the `chromadb` client initializes successfully.
- For file processing errors, verify uploaded files are supported formats: `pdf`, `csv`, `pptx`, `ppt`, `txt`.

