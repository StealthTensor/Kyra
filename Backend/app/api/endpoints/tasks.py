from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.db.session import get_db
from app.db.models import Task, User

router = APIRouter()

@router.get("/")
async def list_tasks(email: str, db: AsyncSession = Depends(get_db)):
    """
    List tasks for a user (by email).
    """
    try:
        # Find User
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Find Tasks
        stmt = select(Task).where(Task.user_id == user.id).order_by(desc(Task.created_at))
        result = await db.execute(stmt)
        tasks = result.scalars().all()
        
        return [
            {
                "id": str(t.id),
                "title": t.description,
                "time": t.due_date.isoformat() if t.due_date else "No due date",
                "type": t.task_type or "task",
                "status": t.status,
                "priority": t.priority
            }
            for t in tasks
        ]
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))
