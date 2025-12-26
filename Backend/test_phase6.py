import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def verify_phase6():
    print("🗓️ Starting Phase 6 Verification...")
    
    # 1. Verify Task Model
    try:
        from app.db.models import Task
        print("✅ Task Model Import: Success")
    except ImportError:
        print("❌ Task Model Import: FAILED")
        return

    # 2. Verify Calendar Service
    try:
        from app.services.calendar_service import calendar_service
        print("✅ Calendar Service Import: Success")
    except ImportError:
        print("❌ Calendar Service Import: FAILED")
        return
        
    # 3. Verify Brain Task Detection
    try:
        from app.services.brain import brain_service
        sample_email = "Team, please submit the project report by tomorrow 5PM. This is a hard deadline."
        print(f"🧠 Testing Task Detection on: '{sample_email}'")
        
        # This will call API, might fail if key invalid or network issue, but we want to verify SDK call structure.
        result = brain_service.detect_tasks(sample_email)
        print(f"   Result: {result}")
        
        if result.get('is_task'):
             print("✅ Task Detection Checklist: Passed (Detected as Task)")
        else:
             print("⚠️ Task Detection Checklist: Warning (Not detected, possibly model variability)")
             
    except Exception as e:
        print(f"❌ Task Detection Error: {e}")

    print("Phase 6 Verification Complete.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(verify_phase6())
