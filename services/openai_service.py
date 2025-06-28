import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a movie recommendation assistant. Recommend movies based on user requests."
}

def get_assistant_reply(conversation):
    conversation = [SYSTEM_MESSAGE] + conversation
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation
    )
    return response.choices[0].message.content
