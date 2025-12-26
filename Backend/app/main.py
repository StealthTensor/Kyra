from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.config import settings
from app.db.session import get_db
from app.services.gmail import gmail_service
from app.services.brain import brain_service

app = FastAPI(title=settings.PROJECT_NAME)

# Set up CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://kyra.ai", # Production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.endpoints import interactions, gmail
from app.api.routers import chat
app.include_router(interactions.router, prefix=settings.API_V1_STR, tags=["interactions"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(gmail.router, prefix=f"{settings.API_V1_STR}/gmail", tags=["gmail"])

@app.get("/")
async def root():
    return {"message": "Email AI OS Backend is running", "docs": "/docs"}

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Simple query to check DB connection
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}

@app.get(f"{settings.API_V1_STR}/auth/login")
async def login():
    auth_url, state = gmail_service.get_auth_url()
    return RedirectResponse(auth_url)

@app.get(f"{settings.API_V1_STR}/auth/callback")
async def callback(code: str, db: AsyncSession = Depends(get_db)):
    print(f"👉 Callback hit with code: {code[:10]}...")
    try:
        print("1. Exchanging code for credentials...")
        creds = await gmail_service.get_credentials_from_code(code)
        
        # Build service to get email address
        print("2. Fetching user profile...")
        service = gmail_service.build_service(creds)
        profile = gmail_service.get_profile(service)
        email_address = profile['emailAddress']
        
        # Database Operations
        from app.db.models import User, Account
        from sqlalchemy import select
        
        # 1. Check if user exists
        result = await db.execute(select(User).where(User.email == email_address))
        user = result.scalars().first()
        
        if not user:
            user = User(email=email_address)
            db.add(user)
            await db.flush()
        
        # 2. Update/Create Account
        result = await db.execute(select(Account).where(Account.email_address == email_address))
        account = result.scalars().first()
        
        if not account:
            account = Account(
                user_id=user.id,
                email_address=email_address,
                access_token=creds.token,
                refresh_token=creds.refresh_token or "",
                expires_at=creds.expiry,
                provider='gmail'
            )
            db.add(account)
        else:
            account.access_token = creds.token
            if creds.refresh_token:
                account.refresh_token = creds.refresh_token
            account.expires_at = creds.expiry
            
        await db.commit()
        await db.refresh(account)
        
        # Redirect to Frontend with User Info
        # In a real app, generate a JWT here. For MVP, we pass simple user data.
        frontend_url = "http://localhost:3000/auth/callback"
        user_param = f"user_id={user.id}&email={email_address}&name={email_address.split('@')[0]}"
        # For security in prod, use a secure HTTPOnly cookie or hash. 
        # Here we just pass it to hydrate the store.
        return RedirectResponse(f"{frontend_url}?{user_param}&token=mvp_token_{user.id}")

    except Exception as e:
        print(f"❌ Callback ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.get(f"{settings.API_V1_STR}/gmail/sync")
async def sync_emails(email: str, db: AsyncSession = Depends(get_db)):
    """
    Trigger manual sync for a user email.
    """
    from app.db.models import Account, Email
    from sqlalchemy import select
    from google.oauth2.credentials import Credentials
    import datetime

    # 1. Get Account
    result = await db.execute(select(Account).where(Account.email_address == email))
    account = result.scalars().first()
    
    if not account:
        return {"error": "Account not found"}
    
    # 2. Reconstruct Credentials
    creds = Credentials(
        token=account.access_token,
        refresh_token=account.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/userinfo.email']
    )
    
    # 3. Build Service 
    try:
        service = gmail_service.build_service(creds)
        
        # 3.1 Get Profile for historyId (Latest State)
        profile = gmail_service.get_profile(service)
        current_history_id = profile.get('historyId')
        
        # 3.2 Fetch Emails
        # LIMITATION: This fetches raw latest 50. 
        # Ideally we use historyId to fetch ONLY what changed if account.last_sync_id exists.
        # But per Phase 1 instructions: "Fetch the last 50 emails" initially.
        emails_data = gmail_service.fetch_emails(service, limit=50)
        
        count = 0
        new_emails_list = []
        new_email_objects = {}
        
        for email_doc in emails_data:
            # Check if exists
            result = await db.execute(select(Email).where(Email.gmail_id == email_doc['gmail_id']))
            existing = result.scalars().first()
            
            if not existing:
                new_email = Email(
                    account_id=account.id,
                    gmail_id=email_doc['gmail_id'],
                    thread_id=email_doc['thread_id'],
                    sender=email_doc['metadata']['from'],
                    subject=email_doc['metadata']['subject'],
                    body_plain=email_doc['content']['cleaned_text'],
                    received_at=datetime.datetime.fromisoformat(email_doc['metadata']['timestamp']),
                    importance_score=0,
                    category='Unprocessed'
                )
                db.add(new_email)
                count += 1
                
                # Add to batch for classification
                new_emails_list.append(email_doc)
                new_email_objects[email_doc['gmail_id']] = new_email

        # 4. Batch Classify New Emails
        if new_emails_list:
            print(f"🧠 Classifying {len(new_emails_list)} new emails...")
            try:
                classification_map = brain_service.classify_emails_batch(new_emails_list)
                
                for gmail_id, result_data in classification_map.items():
                    if gmail_id in new_email_objects:
                        email_obj = new_email_objects[gmail_id]
                        email_obj.importance_score = result_data.get('score', 0)
                        email_obj.category = result_data.get('category', 'Uncategorized')
                        email_obj.explanation = result_data.get('explanation', '')
                        email_obj.confidence = result_data.get('confidence', 0.0)
                        
                        print(f"   scored {email_obj.importance_score}/100: {email_obj.subject[:30]}...")
            except Exception as e:
                print(f"❌ Classification Error: {e}")

        # 5. Task Detection for New Emails
        if new_email_objects:
            print(f"🕵️ Detecting tasks in {len(new_email_objects)} new emails...")
            from app.db.models import Task
             
            for gmail_id, email_obj in new_email_objects.items():
                # Only check if it's Important or Critical to save tokens/time? 
                # Or check all? "Soft tasks" might be in FYI. Let's check all for now or filter > 30 score.
                if email_obj.importance_score >= 30:
                    content_for_task = f"Subject: {email_obj.subject}\nBody: {email_obj.body_plain[:2000]}"
                    task_data = brain_service.detect_tasks(content_for_task)
                     
                    if task_data.get('is_task'):
                        print(f"   ✅ Task found: {task_data.get('description')}")
                        new_task = Task(
                            user_id=account.user_id,
                            email_id=email_obj.id,
                            description=task_data.get('description'),
                            task_type=task_data.get('type'),
                            priority=task_data.get('priority'),
                            status='pending'
                        )
                        if task_data.get('due_date'):
                            try:
                                new_task.due_date = datetime.datetime.fromisoformat(task_data.get('due_date'))
                            except:
                                pass
                         
                        db.add(new_task)
            
            # 6. Attachment Parsing & Thread Summarization
            print(f"📎 Processing attachments and threads for {len(new_email_objects)} new emails...")
            from app.db.models import Attachment
            
            threads_to_summarize = set()
            
            for gmail_id, email_obj in new_email_objects.items():
                # Attachments
                doc = next((d for d in emails_data if d['gmail_id'] == gmail_id), None)
                if doc and doc['content']['attachments']:
                    for att in doc['content']['attachments']:
                        # Fetch content
                        print(f"   Downloading attachment {att['name']}...")
                        content = gmail_service.get_attachment_content(service, gmail_id, att['id'])
                        if content:
                            extracted_text = attachment_service.parse_attachment(content, att['type'], att['name'])
                            new_att = Attachment(
                                email_id=email_obj.id,
                                filename=att['name'],
                                content_type=att['type'],
                                size=att['size'],
                                extracted_text=extracted_text
                            )
                            db.add(new_att)
                            print(f"   Saved attachment: {att['name']}")
                
                # Collect thread ID for summarization
                if email_obj.thread_id:
                    threads_to_summarize.add(email_obj.thread_id)
            
            # Summarize Threads
            if threads_to_summarize:
                print(f"🧵 Summarizing {len(threads_to_summarize)} threads...")
                for thread_id in threads_to_summarize:
                    try:
                        summary = await summarizer_service.summarize_thread(db, thread_id)
                        if summary:
                            print(f"   Summarized thread {thread_id}")
                    except Exception as e:
                        print(f"   Error summarizing thread {thread_id}: {e}")
        
        # 4. Update Sync State
        if current_history_id:
            account.last_sync_id = str(current_history_id)
        
        await db.commit()
        return {
            "message": "Sync complete", 
            "emails_fetched": len(emails_data), 
            "new_saved": count, 
            "history_id": current_history_id
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.get(f"{settings.API_V1_STR}/brain/backfill")
async def backfill_embeddings(db: AsyncSession = Depends(get_db)):
    """
    Generates embeddings for emails that don't have them yet.
    """
    from app.db.models import Email
    from app.services.brain import brain_service
    from sqlalchemy import select
    
    print("🧠 Starting embedding backfill...")
    
    # 1. Fetch emails with NULL embedding
    result = await db.execute(select(Email).where(Email.embedding == None))
    emails = result.scalars().all()
    
    print(f"Found {len(emails)} emails to process.")
    
    count = 0
    for email in emails:
        # Combine subject and body for the embedding text
        # Truncate to avoid token limits if necessary, but Gemini is generous (1M tokens).
        # We'll use a safe chunk of text.
        text_to_embed = f"Subject: {email.subject}\n\n{email.body_plain[:8000]}"
        
        vector = brain_service.get_embedding(text_to_embed)
        
        if vector:
            email.embedding = vector
            count += 1
            if count % 10 == 0:
                print(f"   Processed {count}...")
    
    await db.commit()
    print(f"✅ Backfill complete. Updated {count} emails.")
    return {"message": "Backfill complete", "updated": count}

    print(f"✅ Backfill complete. Updated {count} emails.")
    return {"message": "Backfill complete", "updated": count}

@app.post(f"{settings.API_V1_STR}/digest/generate")
async def generate_digest_endpoint(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Triggers the generation of the daily digest.
    Expects JSON body: {"user_id": "...", "email": "..."}
    """
    try:
        data = await request.json()
        user_id = data.get('user_id')
        email = data.get('email')
        
        # Resolve user_id if not provided (assume single user or look up by email)
        if not user_id and email:
             from app.db.models import User
             from sqlalchemy import select
             result = await db.execute(select(User).where(User.email == email))
             user = result.scalars().first()
             if user:
                 user_id = user.id
        
        if not user_id:
            return {"error": "user_id or email is required"}
            
        digest = await digest_service.generate_daily_digest(db, user_id, email)
        return {"message": "Digest generated", "content": digest}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
