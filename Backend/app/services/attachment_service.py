import base64
import fitz  # PyMuPDF
import docx
import io
from app.services.gmail import gmail_service

class AttachmentService:
    def parse_attachment(self, file_content, content_type, filename):
        """
        Extracts text from PDF or DOCX content.
        """
        text = ""
        try:
            if "pdf" in content_type:
                with fitz.open(stream=file_content, filetype="pdf") as doc:
                    for page in doc:
                        text += page.get_text()
            elif "wordprocessingml" in content_type or filename.endswith(".docx"):
                doc = docx.Document(io.BytesIO(file_content))
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
            else:
                # Text files or others we can try to decode
                if content_type.startswith("text/"):
                    text = file_content.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Error parsing attachment {filename}: {e}")
            return None
            
        return text.strip() if text.strip() else None

attachment_service = AttachmentService()
