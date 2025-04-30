# test_api.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load keys from .env

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'API test successful!'"}]
    )
    print("OpenAI Response:", response.choices[0].message.content)
except Exception as e:
    print("Error:", e)