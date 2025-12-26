import unittest
import asyncio
from unittest.mock import MagicMock
from app.services.brain import BrainService

class TestPriorityEngine(unittest.TestCase):
    def test_batch_classification_parsing(self):
        """
        Verifies that BrainService.classify_emails_batch correctly parses the LLM JSON response.
        """
        mock_brain = BrainService()
        
        # Mock the client.models.generate_content response
        mock_response = MagicMock()
        mock_response.text = """
        {
            "msg_123": {
                "score": 95,
                "category": "Critical",
                "explanation": "Exam deadline mentioned",
                "confidence": 0.9
            },
            "msg_456": {
                "score": 20,
                "category": "Noise",
                "explanation": "Promotional email",
                "confidence": 0.85
            }
        }
        """
        mock_brain.client.models.generate_content = MagicMock(return_value=mock_response)
        
        # Input data
        emails_input = [
            {
                "gmail_id": "msg_123",
                "metadata": {"from": "prof@srm.edu", "subject": "Exam Date"},
                "content": {"raw_snippet": "Exam is tomorrow"}
            },
            {
                "gmail_id": "msg_456",
                "metadata": {"from": "promo@zomato.com", "subject": "50% Off"},
                "content": {"raw_snippet": "Buy now"}
            }
        ]
        
        # Execute
        result = mock_brain.classify_emails_batch(emails_input)
        
        # Assert
        self.assertIn("msg_123", result)
        self.assertEqual(result["msg_123"]["score"], 95)
        self.assertEqual(result["msg_123"]["category"], "Critical")
        self.assertEqual(result["msg_456"]["score"], 20)
        self.assertEqual(result["msg_456"]["category"], "Noise")
        print("\n✅ Batch Classification Parsing Test Passed")

if __name__ == "__main__":
    unittest.main()
