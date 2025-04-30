import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class Config:
    """
    Central configuration for CustomGPT evaluation system
    Contains API keys, paths, and runtime settings
    """

    # ======================
    # API CONFIGURATION
    # ======================
    CUSTOMGPT_API_KEY = os.getenv('CUSTOMGPT_API_KEY')
    CUSTOMGPT_PROJECT_ID = os.getenv('CUSTOMGPT_DEFAULT_AGENT', "68988")
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Required for GPT-4 evaluation

    # CustomGPT API Endpoint (update if needed)
    CUSTOMGPT_BASE_URL = "https://app.customgpt.ai/api/v1"

    # ======================
    # PATH CONFIGURATION
    # ======================
    ROOT_DIR = Path(__file__).parent.parent  # Project root

    # Data directories
    OUTPUT_DIR = ROOT_DIR / "outputs"
    PROMPT_DIR = ROOT_DIR / "prompts"
    CONFIG_DIR = ROOT_DIR / "config"

    # Evaluation files
    PROMPT_FILE = PROMPT_DIR / "sales_prompts.txt"
    RUBRIC_FILE = CONFIG_DIR / "scoring_rubric.yaml"

    # ======================
    # EVALUATION SETTINGS
    # ======================
    # GPT-4 Evaluation Model
    OPENAI_MODEL = "gpt-4-turbo"
    OPENAI_TEMPERATURE = 0.3  # For consistent scoring

    # Rate limiting (seconds between API calls)
    API_COOLDOWN = 1.0

    # ======================
    # PROPERTIES
    # ======================
    @property
    def prompts(self) -> list[str]:
        """Load or initialize test prompts"""
        if not self.PROMPT_FILE.exists():
            self._init_prompt_file()
        return self._read_prompt_file()

    # ======================
    # PRIVATE METHODS
    # ======================
    def _init_prompt_file(self):
        """Create default prompts file if missing"""
        default_prompts = [
            "How much does a pool installation cost?",
            "What are the benefits of saltwater pools?",
            "Do you offer financing options?",
            "What's the typical installation timeline?",
            "Do you offer maintenance services?"
        ]
        self.PROMPT_DIR.mkdir(exist_ok=True)
        self.PROMPT_FILE.write_text("\n".join(default_prompts))

    def _read_prompt_file(self) -> list[str]:
        """Read prompts from file with validation"""
        content = self.PROMPT_FILE.read_text(encoding='utf-8').strip()
        if not content:
            raise ValueError(f"Prompt file is empty: {self.PROMPT_FILE}")
        return [line for line in content.splitlines() if line.strip()]


# Singleton configuration instance
config = Config()

# Validation check on import
if not config.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is required in .env file")

if not config.CUSTOMGPT_API_KEY:
    raise ValueError("CUSTOMGPT_API_KEY is required in .env file")