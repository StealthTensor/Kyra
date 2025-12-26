from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from app.db.session import get_db
from app.db.models import User, Email, Task, Account
from datetime import datetime, timedelta
from typing import Dict
import time

router = APIRouter()

_stats_cache = {}
_cache_ttl = 60

@router.get("/stats")
async def get_dashboard_stats(
    email: str,
    db: AsyncSession = Depends(get_db)
) -> Dict:
    """
    Get aggregated dashboard statistics for a user.
    Returns: urgent emails count, pending tasks count, upcoming events count, inbox health.
    Cached for 1 minute to reduce DB load.
    """
    try:
        cache_key = f"stats_{email}"
        current_time = time.time()
        
        if cache_key in _stats_cache:
            cached_data, cached_time = _stats_cache[cache_key]
            if current_time - cached_time < _cache_ttl:
                return cached_data
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        yesterday = datetime.now(datetime.timezone.utc) - timedelta(days=1)
        future_date = datetime.now() + timedelta(days=7)
        
        urgent_emails_query = select(func.count(Email.id)).where(
            and_(
                Email.received_at >= yesterday,
                Email.importance_score >= 70,
                Email.account.has(user_id=user.id)
            )
        )
        urgent_emails_result = await db.execute(urgent_emails_query)
        urgent_emails_count = urgent_emails_result.scalar() or 0
        
        pending_tasks_query = select(func.count(Task.id)).where(
            and_(
                Task.user_id == user.id,
                Task.status == 'pending'
            )
        )
        pending_tasks_result = await db.execute(pending_tasks_query)
        pending_tasks_count = pending_tasks_result.scalar() or 0
        
        upcoming_tasks_query = select(func.count(Task.id)).where(
            and_(
                Task.user_id == user.id,
                Task.status == 'pending',
                Task.due_date <= future_date,
                Task.due_date >= datetime.now()
            )
        )
        upcoming_tasks_result = await db.execute(upcoming_tasks_query)
        upcoming_events_count = upcoming_tasks_result.scalar() or 0
        
        total_unread_query = select(func.count(Email.id)).where(
            and_(
                Email.account.has(user_id=user.id),
                Email.importance_score >= 30
            )
        )
        total_unread_result = await db.execute(total_unread_query)
        total_unread_count = total_unread_result.scalar() or 0
        
        total_things = urgent_emails_count + pending_tasks_count + upcoming_events_count
        
        inbox_health_score = 100
        if total_unread_count > 50:
            inbox_health_score = max(0, 100 - ((total_unread_count - 50) * 2))
        elif total_unread_count > 0:
            inbox_health_score = max(0, 100 - (total_unread_count * 1))
        
        result = {
            "urgent_emails": urgent_emails_count,
            "pending_tasks": pending_tasks_count,
            "upcoming_events": upcoming_events_count,
            "total_things": total_things,
            "inbox_health": int(inbox_health_score),
            "total_unread": total_unread_count
        }
        
        _stats_cache[cache_key] = (result, current_time)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_dashboard_stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

