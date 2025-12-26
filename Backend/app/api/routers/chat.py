from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Chat with the agent about your emails.
    """
    try:
        # In a real app we'd get user_id from auth token (Depends(get_current_user))
        # For MVP we trust the request Body or hardcode if single user
        # user_id from request or hardcoded for now if not provided
        user_id = request.user_id 
        
        response = await chat_service.generate_response(
            query=request.query,
            user_id=user_id,
            conversation_id=request.conversation_id,
            db=db
        )
        return response
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
