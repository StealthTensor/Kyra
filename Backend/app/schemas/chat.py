from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class Message(BaseModel):
    role: str
    content: str
    created_at: Optional[datetime] = None

class ChatRequest(BaseModel):
    query: str
    conversation_id: Optional[UUID] = None
    user_id: str # Ideally this comes from auth context, but for MVP simplifying

class ChatResponse(BaseModel):
    response: str
    conversation_id: UUID
    conversation_title: str
    sources: List[str] = [] # List of email subjects or IDs used for context
