import os
from flask import Flask, request, render_template
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = "You are a movie recommendation assistant. Recommend movies based on user requests."
conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

def get_assistant_reply(user_message):
    conversation_history.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation_history
    )
    assistant_reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form["message"]
        assistant_reply = get_assistant_reply(user_input)
    return render_template("chat.html", messages=conversation_history)

if __name__ == "__main__":
    app.run(debug=True)




