import os
from flask import Flask, request, render_template
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

messages = [
    {"role": "system", "content": "You are a movie recommendation assistant. Recommend movies based on user requests."}
]

@app.route("/", methods=["GET", "POST"])
def chat():
    global messages
    if request.method == "POST":
        user_input = request.form["message"]
        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        assistant_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_reply})

    return render_template("chat.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
