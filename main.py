from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

# Load price data
with open("prices.json") as f:
    prices = json.load(f)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.form.get('Body', '').lower().strip()
    resp = MessagingResponse()

    if incoming_msg.startswith("price"):
        parts = incoming_msg.split(" ", 1)
        if len(parts) < 2:
            resp.message("Send 'PRICE <item>' to get the current price.")
        else:
            item = parts[1]
            price = prices.get(item)
            if price:
                resp.message(f"{item.title()} – KSh {price} (average)")
            else:
                resp.message(f"Sorry, {item} not found.")
    else:
        resp.message("Send 'PRICE <item>' to get the current price.")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
