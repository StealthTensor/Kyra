from app.core.config import settings
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime

class CalendarService:
    def build_service(self, access_token, refresh_token):
        # We need ALL scopes here because we might be using tokens that have Gmail + Calendar
        # The credential object will just use what it has.
        from app.services.gmail import SCOPES
        creds = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=SCOPES
        )
        return build('calendar', 'v3', credentials=creds)

    def list_upcoming_events(self, access_token, refresh_token, days=7):
        try:
            service = self.build_service(access_token, refresh_token)
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            
            events_result = service.events().list(
                calendarId='primary', 
                timeMin=now,
                maxResults=10, 
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except Exception as e:
            print(f"Calendar List Error: {e}")
            return []

    def create_event(self, access_token, refresh_token, summary, start_time, end_time, description="Created by Kyra"):
        try:
            service = self.build_service(access_token, refresh_token)
            
            event = {
                'summary': summary,
                'location': 'Online',
                'description': description,
                'start': {
                    'dateTime': start_time, # ISO format
                    'timeZone': 'Asia/Kolkata',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'Asia/Kolkata',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")
            return event
        except Exception as e:
            print(f"Calendar Create Error: {e}")
            raise e

    def check_conflicts(self, access_token, refresh_token, start_time, end_time):
        """
        Simple check: fetch events in the window.
        """
        try:
            service = self.build_service(access_token, refresh_token)
            events_result = service.events().list(
                calendarId='primary', 
                timeMin=start_time,
                timeMax=end_time,
                singleEvents=True
            ).execute()
            return events_result.get('items', [])
        except Exception:
            return []

calendar_service = CalendarService()
