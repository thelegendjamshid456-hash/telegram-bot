from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

TOKEN = "8799766843:AAGjQKYAsSRUQExYWcE1FB4yLEtUROqYyGk"

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        reply = f"You said: {text}"

        requests.post(URL, json={
            "chat_id": chat_id,
            "text": reply
        })

    return {"ok": True}

@app.get("/")
def home():
    return {"status": "running"}
