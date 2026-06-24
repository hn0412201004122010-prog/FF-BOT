from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "ffbot_verify"
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")


@app.route("/")
def home():
    return "FF BOT ONLINE"


@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge

    return "Error", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):

                sender_id = event["sender"]["id"]

                if "message" in event:
                    text = event["message"].get("text", "")

                    send_message(
                        sender_id,
                        f"Bạn vừa gửi: {text}"
                    )

    return "EVENT_RECEIVED", 200


def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v23.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    requests.post(url, json=payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)