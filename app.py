from flask import Flask, request, render_template
from config import OPENAI_API_KEY
from services.openai_service import OpenAIService

app = Flask(__name__)
openai_service = OpenAIService(api_key=OPENAI_API_KEY)

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form["message"]
        openai_service.add_user_message(user_input)
        assistant_reply = openai_service.get_assistant_reply()
    return render_template("chat.html", messages=openai_service.messages)

if __name__ == "__main__":
    app.run(debug=True)

