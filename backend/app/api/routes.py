from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import (
    ChatRequest, ChatResponse, DocumentUploadResponse,
    DocumentListResponse, HealthResponse
)
from app.services.chat_service import ChatService
from app.services.document_service import DocumentService
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
chat_service = ChatService()
document_service = DocumentService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Chat endpoint with agent"""
    try:
        response = await chat_service.process_message(
            message=request.message,
            session_id=request.session_id,
            db=db
        )
        return response
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload document for RAG"""
    try:
        result = await document_service.upload_document(file, db)
        return result
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents", response_model=List[DocumentListResponse])
async def list_documents(db: Session = Depends(get_db)):
    """List all uploaded documents"""
    try:
        documents = document_service.list_documents(db)
        return documents
    except Exception as e:
        logger.error(f"List documents error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document"""
    try:
        result = document_service.delete_document(document_id, db)
        return {"message": "Document deleted successfully"}
    except Exception as e:
        logger.error(f"Delete document error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Check database
        db.execute("SELECT 1")
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    
    return {
        "status": "healthy",
        "database": db_status,
        "vector_store": "healthy",
        "openai": "healthy"
    }
