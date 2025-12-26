from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.db.session import get_db
from app.services.digest_service import digest_service
from app.db.models import DailyDigest, User

router = APIRouter()

@router.post("/generate")
async def generate_digest_endpoint(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Triggers the generation of the daily digest.
    Expects JSON body: {"user_id": "...", "email": "..."}
    """
    try:
        data = await request.json()
        user_id = data.get('user_id')
        email = data.get('email')
        
        # Resolve user_id if not provided
        if not user_id and email:
             result = await db.execute(select(User).where(User.email == email))
             user = result.scalars().first()
             if user:
                 user_id = user.id
        
        if not user_id:
            return {"error": "user_id or email is required"}
            
        digest = await digest_service.generate_daily_digest(db, user_id, email)
        return {"message": "Digest generated", "content": digest}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@router.get("/latest")
async def get_latest_digest(email: str, db: AsyncSession = Depends(get_db)):
    """
    Get the latest generated digest for a user (by email).
    """
    try:
        # Find User
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Find Latest Digest
        stmt = select(DailyDigest).where(DailyDigest.user_id == user.id).order_by(desc(DailyDigest.created_at))
        result = await db.execute(stmt)
        digest = result.scalars().first()
        
        if not digest:
            return {"found": False, "content": "No digest generated yet today."}
            
        return {
            "found": True, 
            "content": digest.content, 
            "date": digest.date.isoformat(), 
            "created_at": digest.created_at.isoformat()
        }
    except Exception as e:
        print(f"Error fetching digest: {e}")
        raise HTTPException(status_code=500, detail=str(e))
