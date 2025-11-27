from app.agents.manager_agent import ManagerAgent
from app.models.database_models import Conversation
from sqlalchemy.orm import Session
import uuid
import json
import logging

logger = logging.getLogger(__name__)


class ChatService:
    """Service for handling chat operations"""
    
    def __init__(self):
        self.manager_agent = ManagerAgent()
    
    async def process_message(
        self,
        message: str,
        session_id: str,
        db: Session
    ) -> dict:
        """Process chat message through manager agent"""
        
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Process through manager agent
        result = self.manager_agent.process_message(message, session_id)
        
        # Save to conversation history
        try:
            conversation = Conversation(
                session_id=session_id,
                user_message=message,
                agent_response=result.get("message", ""),
                tool_used=result.get("tool_used"),
                extra_data=result.get("metadata", {})  # Renamed from metadata
            )
            db.add(conversation)
            db.commit()
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            db.rollback()
        
        return result
