from google import genai
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class BrainService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = 'text-embedding-004'

    def get_embedding(self, text: str):
        """
        Generates a vector embedding for the given text.
        """
        try:
            # New SDK usage
            result = self.client.models.embed_content(
                model=self.model,
                contents=text,
                config={'output_dimensionality': 768} # Ensure 768 dims
            )
            # The result object has an 'embeddings' attribute which is a list.
            # We want the first one's values.
            return result.embeddings[0].values
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None

    def classify_emails_batch(self, emails_data: list):
        """
        Classifies a batch of emails using Gemini.
        Returns a dict mapped by gmail_id with score, category, explanation, confidence.
        """
        if not emails_data:
            return {}

        prompt = """
        You are a highly intelligent Email Priority Engine for a CS Student at SRM University.
        Your goal is to classify emails into one of 4 buckets:
        - Critical (Score 85-100): Exam, Deadline, Placement, Security, OTP.
        - Important (Score 60-84): Lab, Faculty, Project, Hackathon, Internship.
        - FYI (Score 30-59): General updates, Newsletters, Events.
        - Noise (Score 0-29): Spam, Promotions, Social Media.

        **Rules**:
        - VIP Domains: @srmist.edu.in, @academia.edu, @google.com -> Boost score.
        - Spam Keywords: Zomato, Offer, Discount -> Kill score.
        - "Vertex" is the user's project name -> HIGH PRIORITY.
        
        **Input Format**:
        ID: <gmail_id>
        From: <sender>
        Subject: <subject>
        Snippet: <snippet>
        ...

        **Output Format**:
        Return a JSON object where keys are the gmail_id and values are objects with:
        - score (int 0-100)
        - category (string)
        - explanation (string, max 15 words)
        - confidence (float 0.0-1.0)
        """
        
        user_content = ""
        for email in emails_data:
            user_content += f"ID: {email['gmail_id']}\\nFrom: {email['metadata']['from']}\\nSubject: {email['metadata']['subject']}\\nSnippet: {email['content']['raw_snippet'][:200]}\\n__\\n"

        try:
            # We use generation config to enforce JSON
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[prompt, user_content],
                config={
                    'response_mime_type': 'application/json'
                }
            )
            
            import json
            result = json.loads(response.text)
            return result
        except Exception as e:
            logger.error(f"Error classifying batch: {e}")
            return {}

    def generate_answer(self, prompt: str):
        """
        Generates a plain text response for a given prompt using Gemini.
        """
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return "I'm sorry, I encountered an error while processing your request."

    def detect_tasks(self, email_text: str):
        """
        Analyzes email content to detect tasks.
        Returns a JSON object with:
        - is_task (bool)
        - description (str)
        - type (deadline/meeting/task)
        - due_date (ISO str or null)
        - priority (high/medium/low)
        """
        prompt = """
        Analyze the following email content and extract any actionable TASKS, DEADLINES, or MEETING requests.
        
        Task Types:
        - "deadline": Hard deadlines (submission, due by, last date).
        - "meeting": Requests to meet (zoom, in-person, time slots).
        - "task": Soft action items (review, read, check).
        
        Rules:
        - If clear date/time is mentioned, extract it in ISO 8601 format (approximate if needed, assume current year 2025).
        - If "Vertex", "GitHub", "Vercel" mentioned -> Priority "high".
        - If "Manual" or "Procedure" attachment implied -> Task "Read [Subject] Manual".
        
        Output JSON:
        {
          "is_task": boolean,
          "description": "short description",
          "type": "deadline" | "meeting" | "task" | null,
          "due_date": "YYYY-MM-DDTHH:MM:SS" | null,
          "priority": "high" | "medium" | "low"
        }
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[prompt, email_text],
                config={'response_mime_type': 'application/json'}
            )
            import json
            result = json.loads(response.text)
            if isinstance(result, list):
                return result[0] if result else {"is_task": False}
            return result
        except Exception as e:
            logger.error(f"Task detection error: {e}")
            return {"is_task": False}

    def summarize_thread(self, thread_content: str):
        """
        Summarizes a long email thread.
        """
        prompt = """
        You are an expert executive assistant. Summarize the following email thread into a concise 3-4 sentence paragraph.
        Focus on:
        - The main issue/topic
        - Who said what (briefly)
        - The current status or next action item
        
        Keep it professional and objective.
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[prompt, thread_content]
            )
            return response.text
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            return "Unable to generate summary."

    def generate_digest(self, context: str):
        """
        Generates a Daily Briefing from a given context of emails and tasks.
        """
        prompt = """
        You are 'Kyra', a highly intelligent Personal AI OS for a busy CS student.
        Generate a "Morning Briefing" based on the following context (Urgent Emails & Tasks).
        
        Style Guide:
        - Tone: Professional, slightly crisp, direct. No fluff.
        - Structure:
          1. "Good Morning. Here is your briefing for [Date]."
          2. Top Priorities (Combine urgent emails and deadlines).
          3. FYI / Notice (Less critical items).
          4. "Good luck today."
        
        Keep it under 200 words. Use bullet points.
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[prompt, context]
            )
            return response.text
        except Exception as e:
            logger.error(f"Digest generation error: {e}")
            return "Unable to generate digest."

brain_service = BrainService()
