import asyncio
from sqlalchemy import text
from app.db.session import AsyncSessionLocal

async def check_db():
    async with AsyncSessionLocal() as db:
        try:
            print("Checking DB connection...")
            await db.execute(text("SELECT 1"))
            print("✅ Database Connected!")
            
            print("Checking Users table...")
            result = await db.execute(text("SELECT count(*) FROM users"))
            count = result.scalar()
            print(f"✅ Users count: {count}")
            
            print("Checking Emails table...")
            result = await db.execute(text("SELECT count(*) FROM emails"))
            count = result.scalar()
            print(f"✅ Emails count: {count}")
            
            if count == 0:
                print("⚠️  Emails table is empty. Please run the Sync.")
            else:
                print("🎉 Emails found!")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_db())
