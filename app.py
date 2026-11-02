from flask import Flask, request
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "slig_verify_2026")
ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.route("/", methods=["GET"])
def home():
    return "S LIG CYBER SECURITY BOT ONLINE 🐉"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        messages = data["entry"][0]["changes"][0]["value"].get("messages", [])

        for message in messages:
            sender = message["from"]

            reply = (
                "Welcome to S LIG CYBER SECURITY! 🐉\n\n"
                "1. Cyber Security\n"
                "2. Online Safety\n"
                "3. Phishing Awareness\n"
                "4. Ethical Hacking Education"
            )

            send_message(sender, reply)

    except (KeyError, IndexError, TypeError):
        pass

    return "EVENT_RECEIVED", 200

def send_message(number, message):
    if not ACCESS_TOKEN or not PHONE_NUMBER_ID:
        return

    url = f"https://graph.facebook.com/vXX.X/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {"body": message}
    }

    requests.post(url, headers=headers, json=payload, timeout=15)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
