from flask import Flask, request
import requests
import os
import telegram

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

JOBS = "jobs"
RESULTS = "results"

os.makedirs(JOBS, exist_ok=True)
os.makedirs(RESULTS, exist_ok=True)

@app.route("/")
def home():
    return "Server Running"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message:
        chat_id = update.message.chat.id

        if update.message.text:
            bot.send_message(chat_id, f"You said: {update.message.text}")

        if update.message.document:
            file = update.message.document
            job_id = "test123"

            file_path = f"{JOBS}/{job_id}.bin"

            new_file = bot.get_file(file.file_id)
            new_file.download(file_path)

            bot.send_message(chat_id, "Queued for processing...")

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
