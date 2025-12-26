import asyncio
import httpx
from uuid import uuid4

# Config
API_URL = "http://127.0.0.1:8000"

async def test_interaction():
    print("🧪 Testing Interaction Logging...")
    
    # We need a valid email ID. For now, we'll try to fetch one from the DB or just use a random one and expect 404 test.
    # Ideally, we should fetch a real email first.
    # But to be self-contained, let's assume we can fetch the list of emails first.
    
    async with httpx.AsyncClient() as client:
        # 1. Fetch an email (we assume the server is running and has data)
        # We don't have a direct "list emails" endpoint in the main.py visible yet?
        # Check main.py... it has /gmail/sync and /brain/backfill. 
        # It doesn't seem to have a simple 'GET /emails' endpoint exposed in the snippet I saw.
        # So testing might be tricky without direct DB access or an endpoint.
        # Let's add a temporary endpoint or use direct DB access in this script.
        pass

# Redoing the script to use direct DB access to get an ID, then hit the API.
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.db.session import AsyncSessionLocal
from app.db.models import Email
from sqlalchemy import select

async def main():
    email_id = None
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Email).limit(1))
        email = result.scalars().first()
        if email:
            email_id = email.id
            print(f"✅ Found email ID: {email_id}")
        else:
            print("❌ No emails found in DB. Run sync first.")
            return

    if email_id:
        url = f"{API_URL}/api/v1/emails/{email_id}/interaction"
        payload = {"action": "open"}
        
        print(f"👉 Sending POST to {url}")
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload)
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.json()}")
            
            if resp.status_code == 200:
                print("✅ Interaction logged successfully!")
            else:
                print("❌ Failed to log interaction.")

if __name__ == "__main__":
    asyncio.run(main())
