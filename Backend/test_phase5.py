import sys
import os
import asyncio

# Add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.services.draft_service import draft_service
    from app.api.endpoints.gmail import DraftRequest, SendRequest
    from app.services.gmail import gmail_service
    from app.services.gmail import SCOPES
    
    print("✅ Imports successful.")
    
    if 'https://www.googleapis.com/auth/gmail.send' in SCOPES:
        print("✅ Send scope present.")
    else:
        print("❌ Send scope MISSING.")
        
    print("Phase 5 Static Check Passed.")

except Exception as e:
    print(f"❌ Check Failed: {e}")
    import traceback
    traceback.print_exc()
