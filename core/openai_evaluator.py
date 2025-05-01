import json
import os
import streamlit as st
<<<<<<< HEAD
from openai import OpenAI
from config import config
=======
import openai  # fix this import
>>>>>>> clean-main

class OpenAIScorer:
    def __init__(self, criteria: dict):
        self.criteria = criteria

        api_key = st.session_state.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing. Please enter it in the Connections tab.")

<<<<<<< HEAD
        self.client = OpenAI(api_key=api_key)
=======
        openai.api_key = api_key  # set the global API key
>>>>>>> clean-main

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
<<<<<<< HEAD
        - feedback: 1-2 sentence per metric
        """

        result = self.client.chat.completions.create(
=======
        - feedback: 1-2 sentences per metric
        """

        result = openai.chat.completions.create(  # call directly on openai
>>>>>>> clean-main
            model=os.getenv("OPENAI_MODEL", "gpt-4-turbo"),
            messages=[
                {"role": "system", "content": "You are a rigorous AI evaluator. Score strictly against the rubric."},
                {"role": "user", "content": evaluation_prompt}
            ],
<<<<<<< HEAD
            response_format={"type": "json_object"},
=======
>>>>>>> clean-main
            temperature=0.0
        )

        return json.loads(result.choices[0].message.content)
<<<<<<< HEAD


=======
>>>>>>> clean-main
