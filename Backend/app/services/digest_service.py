from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.db.models import Email, DailyDigest, Task, Account
from app.services.brain import brain_service
from app.services.gmail import gmail_service
from app.services.calendar_service import calendar_service
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
                    Email.importance_score >= 70
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
        calendar_events = []
        result = await db.execute(select(Account).where(Account.user_id == user_id))
        account = result.scalars().first()
        
        if account and account.access_token and account.refresh_token:
            try:
                events = calendar_service.list_upcoming_events(
                    account.access_token,
                    account.refresh_token,
                    days=1
                )
                today = datetime.datetime.now().date()
                for event in events:
                    start = event.get('start', {}).get('dateTime') or event.get('start', {}).get('date')
                    if start:
                        try:
                            event_date = datetime.datetime.fromisoformat(start.replace('Z', '+00:00')).date()
                            if event_date == today:
                                calendar_events.append(event)
                        except:
                            pass
            except Exception as e:
                print(f"Error fetching calendar events for digest: {e}")
        
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
            due_info = f" (Due: {task.due_date.strftime('%Y-%m-%d')})" if task.due_date else ""
            context += f"- {task.description} (Priority: {task.priority}){due_info}\n"
        
        context += "\nCALENDAR EVENTS (TODAY):\n"
        if not calendar_events:
            context += "No calendar events today.\n"
        for event in calendar_events:
            summary = event.get('summary', 'Untitled Event')
            start = event.get('start', {}).get('dateTime') or event.get('start', {}).get('date', '')
            if start:
                try:
                    start_dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                    time_str = start_dt.strftime('%I:%M %p')
                except:
                    time_str = start
            else:
                time_str = "All day"
            context += f"- {summary} at {time_str}\n"
            
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
