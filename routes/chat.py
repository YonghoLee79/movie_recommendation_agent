from flask import Blueprint, render_template, request, session
from services.openai_service import get_assistant_reply

chat_bp = Blueprint('chat', __name__)

@chat_bp.route("/", methods=["GET", "POST"])
def chat():
    if "messages" not in session:
        session["messages"] = []

    if request.method == "POST":
        user_input = request.form["message"]
        session["messages"].append({"role": "user", "content": user_input})

        assistant_reply = get_assistant_reply(session["messages"])
        session["messages"].append({"role": "assistant", "content": assistant_reply})

    return render_template("chat.html", messages=session["messages"])
