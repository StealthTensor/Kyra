from bs4 import BeautifulSoup
import re

class EmailParser:
    @staticmethod
    def clean_text(html_content: str) -> str:
        """
        Extracts clean text from HTML, removing bloat.
        """
        if not html_content:
            return ""
            
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style", "head", "title", "meta", "[document]"]):
            script.decompose()
            
        # Get text
        text = soup.get_text(separator="\n")
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text

    @staticmethod
    def extract_snippet(text: str, length: int = 200) -> str:
        return text[:length] + "..." if len(text) > length else text
