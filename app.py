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
        return challenge, 200

    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    print("DATA RECEIVED:", data)

    if data.get("object") == "page":

        for entry in data.get("entry", []):

            for event in entry.get("messaging", []):

                if "message" in event and "text" in event["message"]:

                    sender_id = event["sender"]["id"]
                    text = event["message"]["text"]

                    print(f"User: {text}")

                    if text.lower() == "xin chào":
                        send_message(
                            sender_id,
                            "Xin chào! Tôi là FF Bot 🤖"
                        )
                    else:
                        send_message(
                            sender_id,
                            f"Bạn vừa gửi: {text}"
                        )

    return "EVENT_RECEIVED", 200


def send_message(recipient_id, message_text):

    url = (
        f"https://graph.facebook.com/v23.0/me/messages"
        f"?access_token={PAGE_ACCESS_TOKEN}"
    )

    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }

    response = requests.post(url, json=payload)

    print("SEND STATUS:", response.status_code)
    print("SEND RESPONSE:", response.text)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)