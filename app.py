from flask import Flask, request, render_template
import chat_service

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form["message"]
        chat_service.add_user_message(user_input)
        chat_service.get_assistant_reply()

    return render_template("chat.html", messages=chat_service.get_all_messages())

if __name__ == "__main__":
    app.run(debug=True)



