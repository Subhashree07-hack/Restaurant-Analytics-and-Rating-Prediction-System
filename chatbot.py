import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("AQ.Ab8RN6Jq3vf0AsABehZGFYkqjhRjfkiEKixOsKhOqo6ubFl_rg"))

model = genai.GenerativeModel("gemini-2.5-flash")


def get_chat_response(msg, history):
    try:
        chat = model.start_chat(history=history)

        response = chat.send_message(
            f"""
You are Loan AI Assistant.

Rules:
- Reply only to the latest user message.
- Do not repeat greetings.
- Answer only loan, insurance, banking and finance questions.
- Keep answers short and helpful.

User:
{msg}
"""
        )

        return response.text

    except Exception as e:
        return f"⚠️ AI Error: {e}"