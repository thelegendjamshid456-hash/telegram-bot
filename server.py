from flask import Flask, request
import os, uuid, telegram

TOKEN = "        subprocess.run(["
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

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

    if update.message and update.message.document:
        file = update.message.document
        chat_id = update.message.chat.id

        job_id = str(uuid.uuid4())
        file_path = f"{JOBS}/{job_id}.bin"

        new_file = bot.get_file(file.file_id)
        new_file.download(file_path)

        with open(f"{JOBS}/{job_id}.txt", "w") as f:
            f.write(str(chat_id))

        bot.send_message(chat_id, "Queued for processing...")

    return "ok"
