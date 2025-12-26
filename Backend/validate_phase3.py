import asyncio
import httpx
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import sys

# Setup DB connection directly
db_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://") if "postgresql://" in settings.DATABASE_URL else settings.DATABASE_URL
engine = create_async_engine(db_url, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def validate():
    print("🔍 Starting Phase 3 Validation...")
    
    async with AsyncSessionLocal() as session:
        # 1. Get User Email
        print("1. Fetching user from DB...")
        result = await session.execute(text("SELECT email FROM users LIMIT 1"))
        email = result.scalar()
        
        if not email:
            print("❌ No user found in DB. Please Login first via /api/v1/auth/login")
            return

        print(f"✅ Found user: {email}")

        # 1.5 Delete latest email to force re-sync (for validation)
        print("1.5 Deleting latest email to force re-sync...")
        await session.execute(text("""
            DELETE FROM emails 
            WHERE id = (
                SELECT id FROM emails 
                WHERE account_id IN (SELECT id FROM accounts WHERE email_address = :email) 
                ORDER BY received_at DESC 
                LIMIT 1
            )
        """), {"email": email})
        await session.commit()

        # 2. Trigger Sync
        print(f"\n2. Triggering Sync for {email}...")
        async with httpx.AsyncClient() as client:
            try:
                # Assuming default port 8000
                response = await client.get(
                    f"http://127.0.0.1:8000{settings.API_V1_STR}/gmail/sync",
                    params={"email": email},
                    timeout=60.0 # Give LLM time to process
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Sync Successful!")
                    print(f"   - Emails Fetched: {data.get('emails_fetched')}")
                    print(f"   - New Saved: {data.get('new_saved')}")
                else:
                    print(f"❌ Sync Failed: {response.text}")
                    return
            except Exception as e:
                print(f"❌ API Error (is uvicorn running?): {e}")
                # return  <-- Removed to allow DB inspection

        # 3. Inspect Results
        print("\n3. Inspecting Priority Scores (Top 5 Recent):")
        print("-" * 80)
        print(f"{'Subject':<40} | {'Score':<5} | {'Category':<10} | {'Explanation'}")
        print("-" * 80)
        
        query = text("""
            SELECT subject, importance_score, category, explanation 
            FROM emails 
            WHERE account_id IN (SELECT id FROM accounts WHERE email_address = :email)
            ORDER BY received_at DESC 
            LIMIT 5
        """)
        
        result = await session.execute(query, {"email": email})
        rows = result.fetchall()
        
        if not rows:
            print("No emails found.")
        
        for row in rows:
            subject = (row.subject[:38] + ".." if len(row.subject) > 38 else row.subject) if row.subject else "No Subject"
            importance = row.importance_score if row.importance_score is not None else 0
            category = row.category if row.category else "Uncategorized"
            explanation = (row.explanation[:30] + "..") if row.explanation else ""
            print(f"{subject:<40} | {importance:<5} | {category:<10} | {explanation}")
            
        print("-" * 80)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(validate())
