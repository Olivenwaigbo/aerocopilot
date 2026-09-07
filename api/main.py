from pathlib import Path
import sys
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ---------------------------------------------------------
# AeroCopilot imports
# ---------------------------------------------------------

from src.rag_chain import ask_aerocopilot
from src.retriever import search_documents


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="AeroCopilot API",
    description=(
        "AI-powered aviation knowledge assistant "
        "using Retrieval-Augmented Generation."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# Request models
# ---------------------------------------------------------

class AskRequest(BaseModel):
    question: str
    k: Optional[int] = 4


class SearchRequest(BaseModel):
    query: str
    k: Optional[int] = 4


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AeroCopilot API",
        "version": "1.0.0",
    }


# ---------------------------------------------------------
# Ask AeroCopilot
# ---------------------------------------------------------

@app.post("/ask")
def ask(request: AskRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    if request.k < 1 or request.k > 10:
        raise HTTPException(
            status_code=400,
            detail="k must be between 1 and 10."
        )

    try:

        result = ask_aerocopilot(
            question,
            k=request.k
        )

        return {
            "success": True,
            "question": result.get("question"),
            "answer": result.get("answer"),
            "citations": result.get("citations", []),
            "retrieved_documents": result.get(
                "retrieved_documents",
                []
            ),
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"AeroCopilot error: {str(error)}"
        )


# ---------------------------------------------------------
# Search documents
# ---------------------------------------------------------

@app.post("/search")
def search(request: SearchRequest):

    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    if request.k < 1 or request.k > 10:
        raise HTTPException(
            status_code=400,
            detail="k must be between 1 and 10."
        )

    try:

        results = search_documents(
            query,
            k=request.k
        )

        documents = []

        for document, score in results:

            documents.append({
                "text": document.page_content,
                "source": document.metadata.get(
                    "source",
                    "Unknown source"
                ),
                "page": document.metadata.get(
                    "page",
                    "Unknown page"
                ),
                "chunk_id": document.metadata.get(
                    "chunk_id",
                    "Unknown chunk"
                ),
                "score": round(float(score), 4),
            })

        return {
            "success": True,
            "query": query,
            "count": len(documents),
            "results": documents,
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Search error: {str(error)}"
        )


# ---------------------------------------------------------
# List available documents
# ---------------------------------------------------------

@app.get("/documents")
def list_documents():

    documents_path = BASE_DIR / "data" / "documents"

    if not documents_path.exists():

        return {
            "count": 0,
            "documents": []
        }

    documents = sorted(
        [
            document.name
            for document in documents_path.glob("*.pdf")
        ]
    )

    return {
        "count": len(documents),
        "documents": documents
    }


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "service": "AeroCopilot API",
        "description": "AI-powered aviation knowledge assistant",
        "docs": "/docs",
        "health": "/health",
        "ask": "/ask",
        "search": "/search",
        "documents": "/documents",
    }