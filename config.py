from pathlib import Path

class Config:
    """
    Central configuration for CheckMakeGPT evaluation system
    Contains paths and runtime settings.
    """

    # ======================
    # PATH CONFIGURATION
    # ======================
    ROOT_DIR = Path(__file__).parent.parent  # Project root

    OUTPUT_DIR = ROOT_DIR / "outputs"
    PROMPT_DIR = ROOT_DIR / "prompts"
    CONFIG_DIR = ROOT_DIR / "config"

    PROMPT_FILE = PROMPT_DIR / "sales_prompts.txt"
    RUBRIC_FILE = CONFIG_DIR / "scoring_rubric.yaml"

    # ======================
    # API CONFIGURATION (Non-secret)
    # ======================
    CUSTOMGPT_PROJECT_ID = "68988"  # Default project ID (can be changed in UI later)
    CUSTOMGPT_BASE_URL = "https://app.customgpt.ai/api/v1"

    # ======================
    # EVALUATION SETTINGS
    # ======================
    OPENAI_MODEL = "gpt-4-turbo"
    OPENAI_TEMPERATURE = 0.3
    API_COOLDOWN = 1.0

    # ======================
    # PROPERTIES
    # ======================
    @property
    def prompts(self) -> list[str]:
        if not self.PROMPT_FILE.exists():
            self._init_prompt_file()
        return self._read_prompt_file()

    def _init_prompt_file(self):
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
        content = self.PROMPT_FILE.read_text(encoding='utf-8').strip()
        if not content:
            raise ValueError(f"Prompt file is empty: {self.PROMPT_FILE}")
        return [line for line in content.splitlines() if line.strip()]

config = Config()
