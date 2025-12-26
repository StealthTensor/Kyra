import asyncio
from app.services.brain import brain_service
from app.core.config import settings
import sys

async def debug():
    print("🧠 Debugging Brain Service (Real API Call)...")
    print(f"API Key: {settings.GEMINI_API_KEY[:5]}... (Checked)")
    
    dummy_email = {
        "gmail_id": "test_123",
        "metadata": {
            "from": "professor@srmist.edu.in",
            "subject": "Urgent: End Semester Exam Schedule"
        },
        "content": {
            "raw_snippet": "Please find attached the schedule for the upcoming exams. Attendance is mandatory."
        }
    }
    
    try:
        # List models to see what's available
        print("listing models...")
        # SDK might not have list_models in client.models?
        # Actually client.models.list() 
        # But let's try a simple generation with 'gemini-1.5-pro' or 'gemini-1.5-flash-001'
        
        # Or better: just print the classification error details more clearly
        results = brain_service.classify_emails_batch([dummy_email])
        print("\n✅ API Response:")
        print(results)
    except Exception as e:
        print(f"\n❌ API Error: {e}")
        # Try fallbacks
        fallbacks = ['gemini-1.5-flash-001', 'gemini-1.5-pro', 'models/gemini-1.5-flash']
        for model in fallbacks:
            print(f"Trying fallback: {model}...")
            try:
                brain_service.model = model # Not used in classify_emails_batch directly, need to pass it
                # brain.py hardcodes the model name in the call!
                # So I can't check other models easily without changing brain.py.
                pass
            except:
                pass
                
        # Just fail and I will edit brain.py


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(debug())
