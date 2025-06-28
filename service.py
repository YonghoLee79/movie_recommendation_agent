import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❗ OPENAI_API_KEY is missing. Check your .env file.")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = "You are a movie recommendation assistant. Recommend movies based on user requests."
conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

def get_assistant_reply(user_message):
    conversation_history.append({"role": "user", "content": user_message})
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=conversation_history
        )
        assistant_reply = response.choices[0].message.content
    except Exception as e:
        assistant_reply = f"❗ Error communicating with OpenAI: {e}"

    conversation_history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply


