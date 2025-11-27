from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=5000)
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    message: str
    session_id: str
    tool_used: Optional[str] = None
    data: Optional[List[Dict[str, Any]]] = None
    chart_config: Optional[Dict[str, Any]] = None
    chart_data: Optional[List[Dict[str, Any]]] = None
    sources: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None


class DocumentUploadResponse(BaseModel):
    """Response model for document upload"""
    id: int
    filename: str
    file_size: int
    file_type: str
    chunk_count: int
    upload_date: datetime
    message: str


class DocumentListResponse(BaseModel):
    """Response model for listing documents"""
    id: int
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    chunk_count: int
    upload_date: datetime


class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history"""
    id: int
    session_id: str
    user_message: str
    agent_response: str
    tool_used: Optional[str]
    created_at: datetime


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    database: str
    vector_store: str
    openai: str
