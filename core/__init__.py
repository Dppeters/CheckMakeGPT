import os
from dotenv import load_dotenv
from typing import Dict

load_dotenv()


class AgentConfig:
    def __init__(self, agent_id: str, name: str = ""):
        self.id = agent_id
        self.name = name or f"Agent-{agent_id}"
        self.base_url = f"https://app.customgpt.ai/api/v1/projects/{self.id}"


class Config:
    # API Keys
    OPENAI_KEY = os.getenv('OPENAI_API_KEY')
    CUSTOMGPT_KEY = os.getenv('CUSTOMGPT_API_KEY')

    # Agent Registry
    AGENTS: Dict[str, AgentConfig] = {
        "primary": AgentConfig(
            agent_id=os.getenv('CUSTOMGPT_DEFAULT_AGENT', "68988"),
            name="Primary Sales Agent"
        ),
        # Add more agents here
    }

    # Evaluation
    MIN_CTA_SCORE = 1.5
    PROMPT_DIR = "prompts"
    OUTPUT_DIR = "outputs"


config = Config()
