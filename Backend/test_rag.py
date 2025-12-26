import asyncio
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.session import AsyncSessionLocal
from app.db.models import Email
from app.services.brain import brain_service
from sqlalchemy import select

async def test_rag(query: str):
    print(f"🔎 Searching for: '{query}'")
    
    # 1. Generate Query Embedding
    query_vector = brain_service.get_embedding(query)
    if not query_vector:
        print("❌ Failed to generate embedding for query.")
        return

    async with AsyncSessionLocal() as db:
        # 2. Perform Similarity Search
        # Using pgvector's cosine distance operator (<=>). 
        # We want the closest distance, so we order by it.
        # Note: We can also use l2_distance (<->) or max_inner_product (<#>)
        
        # We need to explicitly cast or use the vector operator
        # SQLAlchemy 2.0 + pgvector style:
        stmt = select(Email).order_by(Email.embedding.cosine_distance(query_vector)).limit(5)
        
        result = await db.execute(stmt)
        matches = result.scalars().all()
        
        print(f"\n✅ Found {len(matches)} matches:\n")
        for i, email in enumerate(matches):
            print(f"{i+1}. [Score: ?] {email.subject} ({email.sender})")
            print(f"   Snippet: {email.body_plain[:100]}...\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_rag.py <query_string>")
        print("Example: python test_rag.py 'security alerts'")
    else:
        query_text = " ".join(sys.argv[1:])
        asyncio.run(test_rag(query_text))
