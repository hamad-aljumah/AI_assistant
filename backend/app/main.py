from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.database import engine, Base
from app.config import get_settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="AI Assistant API",
    description="Multi-agent AI assistant with SQL, RAG, and Dashboard capabilities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("Starting AI Assistant API")
    logger.info(f"OpenAI Model: {settings.openai_model}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Assistant API",
        "version": "1.0.0",
        "docs": "/docs"
    }
