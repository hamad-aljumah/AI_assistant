from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database import Base


class Sales(Base):
    """Sales data table"""
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    branch = Column(String(50))
    customer_type = Column(String(50))
    gender = Column(String(20))
    product_line = Column(String(100))
    unit_price = Column(Numeric(10, 2))
    quantity = Column(Integer)
    payment = Column(String(50))
    rating = Column(Numeric(3, 1))
    total = Column(Numeric(10, 2))  # Computed: unit_price * quantity
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Document(Base):
    """Document metadata table"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)  # Size in bytes
    file_type = Column(String(50))  # pdf, docx, txt, md
    chunk_count = Column(Integer, default=0)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Document metadata (renamed from 'metadata' to avoid SQLAlchemy conflict)
    doc_metadata = Column(JSON, default={})


class Conversation(Base):
    """Conversation history table"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    user_message = Column(Text, nullable=False)
    agent_response = Column(Text, nullable=False)
    tool_used = Column(String(50))  # sql_agent, rag_tool, dashboard_tool
    
    # Additional context (renamed from 'metadata' to avoid SQLAlchemy conflict)
    extra_data = Column(JSON, default={})  # Store sources, charts, etc.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
