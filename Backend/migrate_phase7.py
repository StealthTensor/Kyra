import asyncio
from app.db.session import engine
from app.db.models import Base

async def migrate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Phase 7 tables created successfully.")

if __name__ == "__main__":
    asyncio.run(migrate())
