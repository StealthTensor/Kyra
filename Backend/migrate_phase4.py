import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
import sys

# Use asyncpg
db_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://") if "postgresql://" in settings.DATABASE_URL else settings.DATABASE_URL
engine = create_async_engine(db_url, echo=True)

async def migrate():
    print("🔄 Starting Phase 4 Migration...")
    
    async with engine.begin() as conn:
        print("1. Creating 'conversations' table...")
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS conversations (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL, -- references users(id) handled by app logic or foreign key if exists
                title TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """))

        print("2. Creating 'messages' table...")
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS messages (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
                role TEXT NOT NULL, -- user or assistant
                content TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """))
        
        # We might need to handle User FK if we want strict constraint, 
        # assuming users table exists (Phase 0/1).
        # But IF NOT EXISTS handles re-runs.
        
    print("✅ Migration Complete.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(migrate())
