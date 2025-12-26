import os
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.core.config import settings

# Allow OAuth scope change (Google adds openid automatically)
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/calendar.events',
    'openid'
]

class GmailService:
    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "project_id": "email-agent-39", # from client secret json
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
            }
        }

    def get_auth_url(self):
        flow = Flow.from_client_config(
            self.client_config,
            scopes=SCOPES,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent' # Force refresh token
        )
        return authorization_url, state

    async def get_credentials_from_code(self, code: str):
        flow = Flow.from_client_config(
            self.client_config,
            scopes=SCOPES,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials
        return credentials

    def build_service(self, credentials):
        return build('gmail', 'v1', credentials=credentials)
    
    def get_profile(self, service):
        return service.users().getProfile(userId='me').execute()
    
    def fetch_emails(self, service, limit=50):
        """
        Fetches the last N emails.
        """
        # Removed try-except to debug errors
        results = service.users().messages().list(userId='me', maxResults=limit).execute()
        messages = results.get('messages', [])
        
        email_data_list = []
        
        if not messages:
            print("No messages found.")
            return []
        
        # Chunk messages to avoid 429 (Too many concurrent requests)
        chunk_size = 10
        for i in range(0, len(messages), chunk_size):
            chunk = messages[i:i + chunk_size]
            batch = service.new_batch_http_request()
            
            # Helper to process batch response
            def callback(request_id, response, exception):
                if exception:
                    print(f"Error fetching message {request_id}: {exception}")
                    # Don't raise, just log. We want partial success.
                else:
                    email_data_list.append(self.format_email(response))

            for msg in chunk:
                batch.add(service.users().messages().get(userId='me', id=msg['id'], format='full'), callback=callback)
            
            import time
            try:
                batch.execute()
                time.sleep(0.5) # Be gentle
            except Exception as e:
                print(f"Batch execution error: {e}")

        return email_data_list

    def format_email(self, msg):
        from app.services.parser import EmailParser
        import base64
        import datetime

        payload = msg.get('payload', {})
        headers = payload.get('headers', [])
        
        def get_header(name):
            return next((h['value'] for h in headers if h['name'].lower() == name.lower()), "")

        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        body += base64.urlsafe_b64decode(data).decode()
                elif part['mimeType'] == 'text/html':
                    if not body and part['body'].get('data'):
                         data = part['body'].get('data')
                         html_content = base64.urlsafe_b64decode(data).decode()
                         body = EmailParser.clean_text(html_content)
        elif 'body' in payload and payload['body'].get('data'):
             data = payload['body']['data']
             decoded = base64.urlsafe_b64decode(data).decode()
             if payload['mimeType'] == 'text/html':
                 body = EmailParser.clean_text(decoded)
             else:
                 body = decoded

        attachments = []
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('filename'):
                    attachments.append({
                        "name": part['filename'],
                        "type": part['mimeType'],
                        "size": part['body'].get('size', 0),
                        "id": part['body'].get('attachmentId')
                    })

        internal_date = int(msg['internalDate']) / 1000
        timestamp_iso = datetime.datetime.fromtimestamp(internal_date, datetime.timezone.utc).isoformat()

        return {
            "id": None, 
            "gmail_id": msg['id'],
            "thread_id": msg['threadId'],
            "metadata": {
                "from": get_header("From"),
                "to": [t.strip() for t in get_header("To").split(",")] if get_header("To") else [],
                "subject": get_header("Subject"),
                "timestamp": timestamp_iso
            },
            "content": {
                "cleaned_text": body,
                "raw_snippet": msg.get('snippet', ''),
                "attachments": attachments
            },
            "internal_flags": {
                "is_processed": False,
                "version": 1.0
            }
        }
        
    def get_attachment_content(self, service, message_id, attachment_id):
        """
        Fetches the raw content of an attachment.
        """
        try:
            attachment_data = service.users().messages().attachments().get(
                userId='me', messageId=message_id, id=attachment_id
            ).execute()
            data = attachment_data.get('data')
            if data:
                return base64.urlsafe_b64decode(data)
            return None
        except Exception as e:
            print(f"Error fetching attachment content: {e}")
            return None

    def send_email(self, service, to_email, subject, body_text, thread_id=None):
        """
        Sends an email using the Gmail API.
        """
        from email.mime.text import MIMEText
        import base64

        message = MIMEText(body_text)
        message['to'] = to_email
        message['subject'] = subject
        
        if thread_id:
             # If replying, we should set In-Reply-To and References if we had the parent message ID
             # But the Gmail API mainly uses 'threadId' in the metadata to group it.
             # However, for correct threading clients, we usually need 'References'.
             # For MVP, just sending with threadId param might be enough for Gmail, but let's see.
             # Actually, creating a Draft with threadId is the standard way, but sending directly:
             # We just pass {'raw': ..., 'threadId': thread_id}
             pass

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw}
        
        if thread_id:
            body['threadId'] = thread_id
            
        try:
            message = service.users().messages().send(userId="me", body=body).execute()
            print(f"Message sent: {message['id']}")
            return message
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e

gmail_service = GmailService()
