from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Email
from app.services.brain import brain_service
import logging

logger = logging.getLogger(__name__)

class DraftService:
    async def generate_draft(self, db: AsyncSession, thread_id: str, user_prompt: str, tone: str = "Professional") -> dict:
        # 1. Fetch relevant thread context
        # We fetch the last 3 emails in the thread to give context
        # Note: If thread_id is None, we assume a new email (no context)
        context_text = "No previous context (New Email)."
        
        if thread_id:
            stmt = select(Email).where(Email.thread_id == thread_id).order_by(Email.received_at.desc()).limit(3)
            result = await db.execute(stmt)
            emails = result.scalars().all()
            
            if emails:
                # Sort chronologically for the prompt
                emails = sorted(emails, key=lambda x: x.received_at)
                context_text = ""
                for email in emails:
                    context_text += f"\n---\nFrom: {email.sender}\nDate: {email.received_at}\nSubject: {email.subject}\nBody: {email.body_plain[:1000]}\n"

        # 2. Construct Prompt
        system_prompt = f"""
        You are Kyra, an intelligent email assistant.
        Your task is to DRAFT a reply (or new email) based on the user's instructions.
        
        TONE: {tone}
        
        DIRECTIVES:
        - Do NOT include placeholders like [Your Name]. Use "Sent via Kyra" if you must, or strictly follow user instructions.
        - STRICTLY follow the user's instructions.
        - If replying, reference the context appropriately.
        - Be concise.
        
        OUTPUT FORMAT:
        Return ONLY the email body text. Do not include "Subject:" line.
        """
        
        full_prompt = f"{system_prompt}\n\nCONTEXT:{context_text}\n\nUSER INSTRUCTIONS: {user_prompt}\n\nDRAFT BODY:"
        
        # 3. Generate
        draft_body = brain_service.generate_answer(full_prompt)
        
        return {
            "draft_body": draft_body,
            "thread_id": thread_id
        }

draft_service = DraftService()
