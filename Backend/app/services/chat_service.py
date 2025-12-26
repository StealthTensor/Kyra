from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models import Email, Conversation, Message
from app.services.brain import brain_service
from app.schemas.chat import ChatResponse
from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)

class ChatService:
    async def generate_response(self, query: str, user_id: str, db: AsyncSession, conversation_id: UUID = None) -> ChatResponse:
        # 1. Manage Conversation
        if not conversation_id:
            logger.info("Creating new conversation")
            conversation = Conversation(
                user_id=UUID(user_id),
                title=query[:30] + "..." if len(query) > 30 else query # Simple title generation
            )
            db.add(conversation)
            await db.flush()
            conversation_id = conversation.id
        else:
             # Ensure conversation exists and belongs to user (skipping user check for MVP speed, but good to have)
             pass

        # 2. RAG Retrieval
        query_embedding = brain_service.get_embedding(query)
        sources = []
        context_text = ""
        
        if query_embedding:
            # Search top 5 relevant emails
            # Using Pgvector cosine distance operator <=>
            stmt = select(Email).options(selectinload(Email.attachments)).order_by(Email.embedding.cosine_distance(query_embedding)).limit(5)
            result = await db.execute(stmt)
            relevant_emails = result.scalars().all()
            
            context_parts = []
            for email in relevant_emails:
                att_text = ""
                if email.attachments:
                    att_text = "\nAttachments Content:\n" + "\n".join([f"[{a.filename}]: {a.extracted_text[:400]}..." for a in email.attachments if a.extracted_text])
                
                snippet = f"From: {email.sender}\nSubject: {email.subject}\nContent: {email.body_plain[:500]}\n{att_text}\nDate: {email.received_at}\nImp Score: {email.importance_score}\nExplanation: {email.explanation}"
                context_parts.append(snippet)
                sources.append(email.subject or "No Subject")
            
            context_text = "\n---\n".join(context_parts)
            
            # --- PHASE 6: INJECT SCHEDULE ---
            # If query asks about "schedule", "tomorrow", "today", "tasks", fetch tasks/calendar
            # Simple keyword check for MVP efficiency
            keywords = ["schedule", "tomorrow", "today", "tasks", "due", "deadline", "meeting", "calendar"]
            if any(k in query.lower() for k in keywords):
                from app.db.models import Task, Account
                
                # Fetch Pending Tasks
                stmt_tasks = select(Task).where(Task.user_id == UUID(user_id)).where(Task.status == 'pending').order_by(Task.due_date)
                res_tasks = await db.execute(stmt_tasks)
                tasks = res_tasks.scalars().all()
                
                task_list_str = "\n".join([f"- [Task] {t.description} (Due: {t.due_date}, Priority: {t.priority})" for t in tasks])
                
                # Fetch Calendar Events (Next 3 days)
                # Need account access token. Assume single account for MVP
                try:
                    stmt_acc = select(Account).where(Account.user_id == UUID(user_id))
                    res_acc = await db.execute(stmt_acc)
                    account = res_acc.scalars().first()
                    
                    if account:
                        from app.services.calendar_service import calendar_service
                        events = calendar_service.list_upcoming_events(account.access_token, account.refresh_token, days=3)
                        
                        event_list_str = "\n".join([f"- [Event] {e['summary']} (Start: {e['start'].get('dateTime', e['start'].get('date'))})" for e in events])
                    else:
                        event_list_str = "No calendar account connected."
                except Exception as e:
                    event_list_str = f"Error fetching calendar: {str(e)}"

                context_text += f"\n\n=== OVERRIDE CONTEXT: LIVE SCHEDULE ===\nPENDING TASKS:\n{task_list_str}\n\nUPCOMING EVENTS:\n{event_list_str}\n=======================================\n"


        # 3. Construct Prompt with Persona
        system_prompt = """
        You are Kyra, a high-intelligence email intelligence agent for a busy CS student.
        
        CORE DIRECTIVES:
        1. OBJECTIVE TONE: Be helpful but objective. No emotional fluff ("I'm sorry", "I'd love to").
        2. DATA-BACKED: When answering "Why?", cite specific metadata (Sender, Timestamp, Content).
        3. SRM PROTOCOL: If the user or context involves '@srmist.edu.in', default to a "Respectful/Professional" tone.
        4. NO HALLUCINATION: If you don't know, say "I don't have that information".
        5. AGENTIC GUARDRAILS:
           - Refuse to answer non-email questions (e.g. "Write a poem").
           - Never make promises or decisions on behalf of the user (e.g. "I will attend").
           - Your goal is to *assist*, not *replace* the user's judgment.

        SCHEDULE AWARENESS:
        You have access to the user's TASKS and CALENDAR EVENTS in the context.
        If asked about schedule/deadlines, prioritize this data.
        """
        
        full_prompt = f"{system_prompt}\n\nCONTEXT:\n{context_text}\n\nUSER QUERY: {query}\n\nRESPONSE:"

        # 4. Generate Answer
        answer_text = brain_service.generate_answer(full_prompt)

        # 5. Persist Chat
        user_msg = Message(conversation_id=conversation_id, role="user", content=query)
        ai_msg = Message(conversation_id=conversation_id, role="assistant", content=answer_text)
        
        db.add(user_msg)
        db.add(ai_msg)
        await db.commit()

        # Retrieve title (if it was new)
        # In a real app we might update title based on content, keeping it simple for now.
        stmt_conv = select(Conversation).where(Conversation.id == conversation_id)
        conv_res = await db.execute(stmt_conv)
        conv = conv_res.scalar_one()

        return ChatResponse(
            response=answer_text,
            conversation_id=conversation_id,
            conversation_title=conv.title,
            sources=sources 
        )

chat_service = ChatService()
