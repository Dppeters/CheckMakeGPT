# tester.py
import requests
from datetime import datetime
from config import config

class CustomGPTTester:
    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {config.CUSTOMGPT_API_KEY}"  # Changed from CUSTOMGPT_KEY
        }
        self.base_url = config.CUSTOMGPT_BASE_URL
        self.project_id = config.CUSTOMGPT_PROJECT_ID

    def test_prompt(self, prompt: str) -> dict:
        """Test a single prompt against CustomGPT API"""
        try:
            # 1. Create conversation
            conv_response = requests.post(
                f"{self.base_url}/projects/{self.project_id}/conversations",
                headers=self.headers,
                json={"name": f"Test-{datetime.now().strftime('%H%M%S')}"}
            )
            conv_response.raise_for_status()
            session_id = conv_response.json()["data"]["session_id"]

            # 2. Send message
            msg_response = requests.post(
                f"{self.base_url}/projects/{self.project_id}/conversations/{session_id}/messages",
                headers=self.headers,
                json={
                    "response_source": "default",
                    "prompt": prompt
                }
            )
            msg_response.raise_for_status()

            return {
                "success": True,
                "response": msg_response.json()["data"]["openai_response"],
                "conversation_id": session_id
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "conversation_id": None
            }