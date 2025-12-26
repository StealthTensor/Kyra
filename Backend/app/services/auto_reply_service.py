from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Email
from app.services.brain import brain_service
from app.services.draft_service import draft_service
import logging

logger = logging.getLogger(__name__)

class AutoReplyService:
    async def suggest_reply(self, db: AsyncSession, email_id: str, tone: str = "Professional") -> dict:
        """
        Analyze an email and suggest an appropriate auto-reply.
        Returns None if no reply is suggested (e.g., informational emails).
        """
        try:
            result = await db.execute(select(Email).where(Email.id == email_id))
            email = result.scalars().first()
            
            if not email:
                return {"suggested": False, "reason": "Email not found"}
            
            analysis_prompt = f"""
            Analyze the following email and determine if an auto-reply would be appropriate.
            
            From: {email.sender}
            Subject: {email.subject}
            Body: {email.body_plain[:2000] if email.body_plain else ""}
            
            Consider:
            1. Is this a question that needs answering?
            2. Is this a request for action/response?
            3. Is this informational only (newsletter, notification, etc.)?
            4. Does it require human judgment or could a simple acknowledgment suffice?
            
            Respond in JSON format:
            {{
                "should_reply": true/false,
                "reason": "brief explanation",
                "reply_type": "acknowledgment" | "quick_answer" | "needs_human" | "none",
                "suggested_tone": "Professional" | "Casual" | "Formal"
            }}
            
            IMPORTANT SAFETY RULES:
            - Do NOT suggest replies for emails that make promises or commitments
            - Do NOT suggest replies with emotional content
            - Do NOT suggest replies that make decisions
            - Only suggest "acknowledgment" or "quick_answer" for simple, safe responses
            """
            
            analysis_result = brain_service.generate_answer(analysis_prompt)
            
            import json
            try:
                analysis_json = json.loads(analysis_result)
            except:
                analysis_json = {"should_reply": False, "reason": "Could not parse analysis"}
            
            if not analysis_json.get("should_reply", False):
                return {
                    "suggested": False,
                    "reason": analysis_json.get("reason", "No reply needed")
                }
            
            reply_type = analysis_json.get("reply_type", "acknowledgment")
            
            if reply_type == "needs_human":
                return {
                    "suggested": False,
                    "reason": "This email requires human judgment and cannot be auto-replied"
                }
            
            suggested_tone = analysis_json.get("suggested_tone", tone)
            
            user_prompt = self._generate_reply_prompt(email, reply_type)
            
            draft_result = await draft_service.generate_draft(
                db,
                email.thread_id,
                user_prompt,
                suggested_tone
            )
            
            return {
                "suggested": True,
                "reply_type": reply_type,
                "draft_body": draft_result["draft_body"],
                "reason": analysis_json.get("reason", "Auto-reply suggested"),
                "confidence": "medium"
            }
            
        except Exception as e:
            logger.error(f"Error in suggest_reply: {e}")
            return {"suggested": False, "reason": f"Error: {str(e)}"}
    
    def _generate_reply_prompt(self, email: Email, reply_type: str) -> str:
        """
        Generate a prompt for the draft service based on reply type.
        """
        if reply_type == "acknowledgment":
            return f"Write a brief acknowledgment email for: {email.subject}. Thank them and let them know you received their message. Keep it professional and concise."
        elif reply_type == "quick_answer":
            subject_lower = email.subject.lower()
            body_preview = email.body_plain[:500] if email.body_plain else ""
            
            if "meeting" in subject_lower or "schedule" in subject_lower:
                return f"Write a brief reply confirming availability or suggesting alternative times for: {email.subject}"
            elif "question" in subject_lower or "?" in body_preview:
                return f"Write a brief, helpful answer to their question about: {email.subject}. Be concise and direct."
            else:
                return f"Write a brief, professional reply to: {email.subject}. Address their main point concisely."
        else:
            return f"Write a brief, professional reply to: {email.subject}"

auto_reply_service = AutoReplyService()

