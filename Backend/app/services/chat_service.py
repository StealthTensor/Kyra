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
    ALLOWED_INTENTS = ["explain", "filter", "teach", "command"]
    
    def _classify_intent(self, query: str) -> dict:
        """
        Classify the user's intent from their query.
        Returns intent classification with allowed/denied flag.
        """
        intent_prompt = f"""
        Classify the intent of this user query related to email management:
        
        Query: "{query}"
        
        Possible intents:
        - explain: Asking "why", "how", or requesting explanation about emails/decisions
        - filter: Asking to show, filter, or find specific emails
        - teach: Teaching preferences, correcting behavior, setting rules
        - command: Asking to perform actions (archive, mark, etc.)
        - chat: General conversation, unrelated questions, creative writing
        
        Respond in JSON format:
        {{
            "intent": "explain" | "filter" | "teach" | "command" | "chat",
            "confidence": "high" | "medium" | "low",
            "reasoning": "brief explanation"
        }}
        """
        
        try:
            result = brain_service.generate_answer(intent_prompt)
            import json
            import re
            
            json_match = re.search(r'\{[^}]+\}', result, re.DOTALL)
            if json_match:
                intent_data = json.loads(json_match.group())
            else:
                intent_data = {"intent": "chat", "confidence": "low", "reasoning": "Could not parse"}
        except Exception as e:
            logger.warning(f"Intent classification failed: {e}")
            intent_data = {"intent": "chat", "confidence": "low", "reasoning": "Classification error"}
        
        intent = intent_data.get("intent", "chat")
        is_allowed = intent in self.ALLOWED_INTENTS
        
        return {
            "intent": intent,
            "is_allowed": is_allowed,
            "confidence": intent_data.get("confidence", "low"),
            "reasoning": intent_data.get("reasoning", "")
        }
    
    async def generate_response(self, query: str, user_id: str, db: AsyncSession, conversation_id: UUID = None) -> ChatResponse:
        try:
            # 0. Intent Validation
            intent_classification = self._classify_intent(query)
            
            if not intent_classification["is_allowed"]:
                intent = intent_classification["intent"]
                error_message = f"I can only help with email management tasks. Your query seems to be: {intent}. "
                error_message += "I can help you with: explaining email decisions, filtering/finding emails, teaching preferences, or executing commands."
                error_message += "\n\nPlease rephrase your query to focus on email management."
                
                return ChatResponse(
                    response=error_message,
                    conversation_id=conversation_id or UUID(str(uuid4())),
                    conversation_title="Intent Rejected",
                    sources=[],
                    intent=intent,
                    intent_rejected=True
                )
            # 1. Manage Conversation
            if not conversation_id:
                logger.info(f"Creating new conversation for user {user_id}")
                try:
                    conversation = Conversation(
                        user_id=UUID(user_id),
                        title=query[:30] + "..." if len(query) > 30 else query
                    )
                    db.add(conversation)
                    await db.flush()
                    conversation_id = conversation.id
                except Exception as e:
                    logger.error(f"Failed to create conversation: {e}")
                    raise e
            
            # 2. RAG Retrieval
            logger.info(f"Generating embedding for query: {query}")
            try:
                query_embedding = brain_service.get_embedding(query)
            except Exception as e:
                logger.error(f"Brain Service Embedding Failed: {e}")
                query_embedding = None # Fallback to no-context chat

            sources = []
            context_text = ""
            
            if query_embedding:
                try:
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
                except Exception as e:
                    logger.error(f"Postgres Vector Search Failed: {e}")
                
                # --- PHASE 6: INJECT SCHEDULE ---
                keywords = ["schedule", "tomorrow", "today", "tasks", "due", "deadline", "meeting", "calendar"]
                if any(k in query.lower() for k in keywords):
                    try:
                        from app.db.models import Task, Account
                        
                        stmt_tasks = select(Task).where(Task.user_id == UUID(user_id)).where(Task.status == 'pending').order_by(Task.due_date)
                        res_tasks = await db.execute(stmt_tasks)
                        tasks = res_tasks.scalars().all()
                        
                        task_list_str = "\n".join([f"- [Task] {t.description} (Due: {t.due_date}, Priority: {t.priority})" for t in tasks])
                        
                        stmt_acc = select(Account).where(Account.user_id == UUID(user_id))
                        res_acc = await db.execute(stmt_acc)
                        account = res_acc.scalars().first()
                        
                        event_list_str = "No calendar account connected."
                        if account:
                            try:
                                from app.services.calendar_service import calendar_service
                                events = calendar_service.list_upcoming_events(account.access_token, account.refresh_token, days=3)
                                event_list_str = "\n".join([f"- [Event] {e['summary']} (Start: {e['start'].get('dateTime', e['start'].get('date'))})" for e in events])
                            except Exception as cal_err:
                                logger.warning(f"Calendar fetch failed: {cal_err}")
                                event_list_str = "Error fetching calendar events."

                        context_text += f"\n\n=== OVERRIDE CONTEXT: LIVE SCHEDULE ===\nPENDING TASKS:\n{task_list_str}\n\nUPCOMING EVENTS:\n{event_list_str}\n=======================================\n"
                    except Exception as e:
                        logger.error(f"Schedule Injection Failed: {e}")


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
            logger.info("Sending prompt to Brain Service...")
            try:
                answer_text = brain_service.generate_answer(full_prompt)
            except Exception as e:
                logger.error(f"Brain Service Generation Failed: {e}")
                answer_text = "I'm having trouble thinking right now. Please check my logs."

            # 5. Persist Chat
            try:
                user_msg = Message(conversation_id=conversation_id, role="user", content=query)
                ai_msg = Message(conversation_id=conversation_id, role="assistant", content=answer_text)
                
                db.add(user_msg)
                db.add(ai_msg)
                await db.commit()
            except Exception as e:
                logger.error(f"Failed to persist chat messages: {e}")
                # Continue, don't break response just for history
            
            # Retrieve title
            try:
                stmt_conv = select(Conversation).where(Conversation.id == conversation_id)
                conv_res = await db.execute(stmt_conv)
                conv = conv_res.scalar_one()
                conv_title = conv.title
            except:
                conv_title = "New Conversation"

            return ChatResponse(
                response=answer_text,
                conversation_id=conversation_id,
                conversation_title=conv_title,
                sources=sources,
                intent=intent_classification.get("intent"),
                intent_rejected=False
            )

        except Exception as e:
            logger.critical(f"CRITICAL ERROR in generate_response: {e}")
            import traceback
            traceback.print_exc()
            raise e

chat_service = ChatService()
