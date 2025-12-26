import asyncio
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import Account
from app.services.gmail import gmail_service
from app.core.config import settings
from google.oauth2.credentials import Credentials

async def debug_gmail_sync(email_input: str):
    print(f"🔍 Debugging Sync for: {email_input}")
    
    async with AsyncSessionLocal() as db:
        # 1. Get Account
        result = await db.execute(select(Account).where(Account.email_address == email_input))
        account = result.scalars().first()
        
        if not account:
            print(f"❌ Account not found for {email_input}")
            # List all accounts to help
            result = await db.execute(select(Account))
            accounts = result.scalars().all()
            print("Available accounts:")
            for acc in accounts:
                print(f" - {acc.email_address}")
            return

        print(f"✅ Found Account ID: {account.id}")
        print(f"ℹ️ Access Token (first 10): {account.access_token[:10]}...")
        print(f"ℹ️ Refresh Token Present: {bool(account.refresh_token)}")
        
        # 2. Reconstruct Credentials
        creds = Credentials(
            token=account.access_token,
            refresh_token=account.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/userinfo.email']
        )
        
        # 3. Test Service
        try:
            print("🚀 Building Gmail Service...")
            service = gmail_service.build_service(creds)
            
            print("👤 Fetching Profile...")
            profile = gmail_service.get_profile(service)
            print(f"✅ Profile Connected: {profile['emailAddress']}")
            print(f"ℹ️ History ID: {profile.get('historyId')}")

            print("📨 Fetching Emails...")
            emails = gmail_service.fetch_emails(service, limit=5) # Limit 5 for debug
            
            print(f"✅ Fetched {len(emails)} emails.")
            if len(emails) > 0:
                print("First email snippet:", emails[0]['content']['raw_snippet'])
            else:
                print("⚠️ Fetched 0 emails. Check your Gmail inbox.")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_sync.py <email_address>")
    else:
        asyncio.run(debug_gmail_sync(sys.argv[1]))
