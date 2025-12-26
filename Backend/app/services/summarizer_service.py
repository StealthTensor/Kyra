from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Email, ThreadSummary
from app.services.brain import brain_service

class SummarizerService:
    async def summarize_thread(self, db: AsyncSession, thread_id: str):
        """
        Summarizes a thread if it has enough messages.
        """
        # Fetch emails in thread
        result = await db.execute(select(Email).where(Email.thread_id == thread_id).order_by(Email.received_at))
        emails = result.scalars().all()
        
        if len(emails) < 3:
            return None
            
        # Check if already summarized recently? 
        # For now, just summarize.
        
        # Prepare context
        thread_content = ""
        for email in emails:
            thread_content += f"From: {email.sender}\nDate: {email.received_at}\nBody: {email.body_plain[:500]}\n---\n"
            
        summary_text = brain_service.summarize_thread(thread_content)
        
        # Save to DB
        result = await db.execute(select(ThreadSummary).where(ThreadSummary.thread_id == thread_id))
        existing = result.scalars().first()
        
        if existing:
            existing.summary = summary_text
            existing.message_count = len(emails)
        else:
            new_summary = ThreadSummary(
                thread_id=thread_id,
                summary=summary_text,
                message_count=len(emails)
            )
            db.add(new_summary)
            
        await db.commit()
        return summary_text

summarizer_service = SummarizerService()
