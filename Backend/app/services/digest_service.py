from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.db.models import Email, DailyDigest, Task
from app.services.brain import brain_service
from app.services.gmail import gmail_service
import datetime

class DigestService:
    async def generate_daily_digest(self, db: AsyncSession, user_id, email_address):
        """
        Generates a daily briefing.
        """
        # 1. Fetch Important emails from last 24h
        yesterday = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
        result = await db.execute(
            select(Email)
            .where(
                and_(
                    Email.received_at >= yesterday,
                    Email.importance_score >= 70 # Arbitrary threshold for "Important"
                )
            )
            .join(Email.account)
            .where(Email.account.has(user_id=user_id))
        )
        emails = result.scalars().all()
        
        # 2. Fetch Tasks (Pending)
        result = await db.execute(
            select(Task)
            .where(and_(Task.user_id == user_id, Task.status == 'pending'))
        )
        tasks = result.scalars().all()
        
        # 3. Fetch Calendar Events (Today)
        # Need to re-instantiate credentials or use CalendarService. 
        # For now, we'll skip live calendar fetch inside this service or mock it, 
        # assuming CalendarService is available. 
        # Let's import CalendarService if possible, or leave it for now.
        # Simplification: Only use Email + Tasks for MVP Digest
        
        context = "Here are the important updates for today:\n\n"
        
        context += "URGENT EMAILS:\n"
        if not emails:
            context += "No urgent emails.\n"
        for email in emails:
            context += f"- [{email.importance_score}] {email.subject} (from {email.sender})\n"
            
        context += "\nPENDING TASKS:\n"
        if not tasks:
            context += "No pending tasks.\n"
        for task in tasks:
            context += f"- {task.description} (Priority: {task.priority})\n"
            
        # Generate Digest
        digest_content = brain_service.generate_digest(context)
        
        # Save
        today = datetime.datetime.now().date()
        daily_digest = DailyDigest(
            user_id=user_id,
            date=today,
            content=digest_content
        )
        db.add(daily_digest)
        await db.commit()
        
        # Build HTML email body
        email_body = f"<h1>Daily Briefing ({today})</h1>\n<p>{digest_content.replace(chr(10), '<br>')}</p>"
        
        # Email it to the user? "The Morning Digest" typically implies an email.
        # But instructions say "Generate a 'Daily Briefing' message".
        # Let's try to email it too, why not.
        
        return digest_content

digest_service = DigestService()
