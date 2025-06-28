import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# 대화 상태
messages = [
    {"role": "system", "content": "You are a movie recommendation assistant. Recommend movies based on user requests."}
]

def add_user_message(user_input):
    messages.append({"role": "user", "content": user_input})

def get_assistant_reply():
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    assistant_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply

def get_all_messages():
    return messages
