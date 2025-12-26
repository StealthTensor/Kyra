import asyncio
import sys
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import User

async def get_user():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        user = result.scalars().first()
        if user:
            print(user.id)
        else:
            print("NO_USER")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_user())
