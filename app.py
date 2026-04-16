from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return {"status": "running"}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        reply = f"You said: {text}"

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )

    return {"ok": True}
