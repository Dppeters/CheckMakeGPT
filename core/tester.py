# tester.py
import requests
from datetime import datetime
from config import config
import streamlit as st  # Required to access session state

class CustomGPTTester:
    def __init__(self):
        api_key = st.session_state.get("CUSTOMGPT_API_KEY")
        if not api_key:
            raise ValueError("CUSTOMGPT_API_KEY is missing. Please enter it in the Connections tab.")

        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {api_key}"
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
