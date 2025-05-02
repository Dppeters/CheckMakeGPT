import json
import os
import re
import streamlit as st
import openai  # use correct import

class OpenAIScorer:
    def __init__(self, criteria: dict):
        self.criteria = criteria

        api_key = st.session_state.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing. Please enter it in the Connections tab.")

        openai.api_key = api_key  # set global API key

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
        - feedback: 1-2 sentences per metric
        """

        result = openai.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4-turbo"),
            messages=[
                {"role": "system", "content": "You are a rigorous AI evaluator. Score strictly against the rubric."},
                {"role": "user", "content": evaluation_prompt}
            ],
            temperature=0.0
        )

        def extract_json(text):
            # Remove Markdown code block markers if present
            text = re.sub(r"```(json)?", "", text, flags=re.IGNORECASE).strip()
            try:
                return json.loads(text)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON from OpenAI response: {e}\nRaw response:\n{text}")

        content = result.choices[0].message.content
        return extract_json(content)
