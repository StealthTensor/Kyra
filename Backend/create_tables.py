from app.db.session import engine
from app.db.models import Base
import asyncio

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created (including tasks)")

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables())
