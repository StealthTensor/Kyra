import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
import sys

# Use asyncpg
db_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://") if "postgresql://" in settings.DATABASE_URL else settings.DATABASE_URL
engine = create_async_engine(db_url, echo=True)

async def migrate():
    print("🔄 Starting Phase 3 Migration...")
    
    async with engine.begin() as conn:
        print("1. Adding 'category' (if missing)...")
        # Note: category might exist from previous attempts or initial schema
        # but we want it as TEXT not String (if that matters in PG, they are similar)
        # We use IF NOT EXISTS logic via catch or check
        try:
            await conn.execute(text("ALTER TABLE emails ADD COLUMN IF NOT EXISTS category TEXT;"))
        except Exception as e:
            print(f" - Note: {e}")

        print("2. Adding 'explanation'...")
        await conn.execute(text("ALTER TABLE emails ADD COLUMN IF NOT EXISTS explanation TEXT;"))
        
        print("3. Adding 'confidence'...")
        await conn.execute(text("ALTER TABLE emails ADD COLUMN IF NOT EXISTS confidence FLOAT;"))
        
    print("✅ Migration Complete.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(migrate())
