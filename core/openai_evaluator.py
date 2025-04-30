import json
import os
from openai import OpenAI
from config import config

class OpenAIScorer:
    def __init__(self, criteria: dict):
        self.criteria = criteria
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def evaluate(self, prompt: str, response: str) -> dict:
        evaluation_prompt = f"""
        Analyze this CustomGPT response against these criteria:

        PROMPT: {prompt}
        RESPONSE: {response}

        RUBRIC:
        {json.dumps(self.criteria, indent=2)}

        Return JSON with:
        - overall_weighted_score (1-10)
        - scores: score for each metric (1-10)
        - feedback: 1-2 sentence per metric
        """

        result = self.client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4-turbo"),
            messages=[
                {"role": "system", "content": "You are a rigorous AI evaluator. Score strictly against the rubric."},
                {"role": "user", "content": evaluation_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )

        return json.loads(result.choices[0].message.content)
