from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "ffbot_verify"

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

    print(data)

    return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)