from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import User, Account, Task
from app.services.calendar_service import calendar_service
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter()

@router.get("/events")
async def get_calendar_events(
    email: str,
    days: int = 7,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    Get upcoming calendar events and tasks combined.
    Returns events from Google Calendar and tasks from database.
    """
    try:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        events = []
        
        result = await db.execute(select(Account).where(Account.user_id == user.id))
        account = result.scalars().first()
        
        if account and account.access_token and account.refresh_token:
            try:
                calendar_events = calendar_service.list_upcoming_events(
                    account.access_token,
                    account.refresh_token,
                    days=days
                )
                
                for event in calendar_events[:limit]:
                    start = event.get('start', {}).get('dateTime') or event.get('start', {}).get('date')
                    if start:
                        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    else:
                        start_dt = datetime.now()
                    
                    events.append({
                        "id": event.get('id'),
                        "title": event.get('summary', 'Untitled Event'),
                        "time": start,
                        "type": "event",
                        "source": "calendar",
                        "description": event.get('description', ''),
                        "location": event.get('location', ''),
                        "start_time": start_dt.isoformat() if isinstance(start_dt, datetime) else start
                    })
            except Exception as e:
                print(f"Error fetching calendar events: {e}")
        
        future_date = datetime.now() + timedelta(days=days)
        
        stmt = select(Task).where(
            Task.user_id == user.id,
            Task.status == 'pending'
        ).order_by(Task.due_date.asc() if Task.due_date else Task.created_at.asc())
        
        result = await db.execute(stmt)
        tasks = result.scalars().all()
        
        for task in tasks:
            if task.due_date and task.due_date <= future_date:
                events.append({
                    "id": str(task.id),
                    "title": task.description or 'Untitled Task',
                    "time": task.due_date.isoformat() if task.due_date else None,
                    "type": task.task_type or "task",
                    "source": "task",
                    "priority": task.priority,
                    "status": task.status,
                    "start_time": task.due_date.isoformat() if task.due_date else None
                })
            elif not task.due_date:
                events.append({
                    "id": str(task.id),
                    "title": task.description or 'Untitled Task',
                    "time": None,
                    "type": task.task_type or "task",
                    "source": "task",
                    "priority": task.priority,
                    "status": task.status,
                    "start_time": None
                })
        
        def get_sort_key(event):
            if event.get("start_time"):
                try:
                    return datetime.fromisoformat(event["start_time"].replace('Z', '+00:00'))
                except:
                    return datetime.max
            return datetime.max
        
        events.sort(key=get_sort_key)
        
        return events[:limit]
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_calendar_events: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/events")
async def create_calendar_event(
    email: str,
    summary: str,
    start_time: str,
    end_time: str,
    description: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a calendar event in Google Calendar.
    Requires user confirmation in production.
    """
    try:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        result = await db.execute(select(Account).where(Account.user_id == user.id))
        account = result.scalars().first()
        
        if not account or not account.access_token or not account.refresh_token:
            raise HTTPException(status_code=404, detail="Account not found or not connected")
        
        event = calendar_service.create_event(
            account.access_token,
            account.refresh_token,
            summary,
            start_time,
            end_time,
            description or "Created by Kyra"
        )
        
        return {"status": "created", "event": event}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating calendar event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conflicts")
async def check_conflicts(
    email: str,
    start_time: str,
    end_time: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Check for scheduling conflicts in the given time range.
    """
    try:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        result = await db.execute(select(Account).where(Account.user_id == user.id))
        account = result.scalars().first()
        
        if not account or not account.access_token or not account.refresh_token:
            raise HTTPException(status_code=404, detail="Account not found or not connected")
        
        conflicts = calendar_service.check_conflicts(
            account.access_token,
            account.refresh_token,
            start_time,
            end_time
        )
        
        return {
            "has_conflicts": len(conflicts) > 0,
            "conflicts": [
                {
                    "id": c.get('id'),
                    "summary": c.get('summary'),
                    "start": c.get('start'),
                    "end": c.get('end')
                }
                for c in conflicts
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error checking conflicts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

