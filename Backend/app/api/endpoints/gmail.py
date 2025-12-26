from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.draft_service import draft_service
from app.services.gmail import gmail_service
from app.db.models import Account
from sqlalchemy import select, desc
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

class DraftRequest(BaseModel):
    thread_id: Optional[str] = None
    prompt: str
    tone: Optional[str] = "Professional"
    email_address: str # identifying user (since we aren't using strict Auth middleware for MVP, we pass email)

class SendRequest(BaseModel):
    email_address: str
    recipient: str 
    subject: str
    body: str
    thread_id: Optional[str] = None

@router.post("/draft")
async def generate_draft_endpoint(request: DraftRequest, db: AsyncSession = Depends(get_db)):
    """
    Generate a draft response based on a prompt and optional thread context.
    """
    try:
        result = await draft_service.generate_draft(db, request.thread_id, request.prompt, request.tone)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send")
async def send_email_endpoint(request: SendRequest, db: AsyncSession = Depends(get_db)):
    """
    Send an email via Gmail API.
    """
    # 1. Get Account
    stmt = select(Account).where(Account.email_address == request.email_address)
    result = await db.execute(stmt)
    account = result.scalars().first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    try:
        from google.oauth2.credentials import Credentials
        from app.core.config import settings
        from app.services.gmail import SCOPES
        
        creds = Credentials(
            token=account.access_token,
            refresh_token=account.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=SCOPES
        )
        
        service = gmail_service.build_service(creds)
        
        sent_msg = gmail_service.send_email(
            service, 
            request.recipient, 
            request.subject, 
            request.body, 
            request.thread_id
        )
        
        return {"status": "sent", "message_id": sent_msg['id']}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/messages")
async def list_messages(
    skip: int = 0, 
    limit: int = 50, 
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    List emails from the database.
    """
    from app.db.models import Email
    
    # Simple query ordering by Importance, then Date
    query = select(Email).order_by(desc(Email.importance_score), desc(Email.received_at))
    
    if category and category != 'All':
        query = query.where(Email.category == category)
        
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    emails = result.scalars().all()
    
    return [
        {
            "id": str(e.id),
            "gmail_id": e.gmail_id,
            "thread_id": e.thread_id,
            "subject": e.subject,
            "from": e.sender,
            "snippet": e.body_plain[:200] if e.body_plain else "",
            "timestamp": e.received_at.isoformat() if e.received_at else "",
            "isRead": False, # Future: Add is_read to DB model. For MVP, assume unread.
            "labels": [e.category] if e.category else [],
            "score": e.importance_score,
            "summary": e.explanation
        }
        for e in emails
    ]

@router.get("/messages/{message_id}")
async def get_message(message_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get a single email by ID (Internal UUID or Gmail ID).
    """
    from app.db.models import Email
    
    # Try ID first (if UUID format), else assume Gmail ID
    try:
        import uuid
        uuid.UUID(message_id)
        query = select(Email).where(Email.id == message_id)
    except ValueError:
        query = select(Email).where(Email.gmail_id == message_id)
    
    result = await db.execute(query)
    email = result.scalars().first()
    
    # Fallback
    if not email:
        query = select(Email).where(Email.gmail_id == message_id)
        result = await db.execute(query)
        email = result.scalars().first()
        
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
        
    return {
        "id": str(email.id),
        "gmail_id": email.gmail_id,
        "thread_id": email.thread_id,
        "subject": email.subject,
        "from": email.sender,
        "body": email.body_plain,
        "timestamp": email.received_at.isoformat() if email.received_at else "",
        "category": email.category,
        "score": email.importance_score,
        "explanation": email.explanation,
        "analysis": email.explanation 
    }
