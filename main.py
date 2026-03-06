from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

app = Flask(__name__)

# Example Kenya food price API
GOV_PRICES_URL = "https://api.foodprices.vam.wfp.org/v1/prices?country_code=KEN"

def get_price(item):
    try:
        response = requests.get(GOV_PRICES_URL)
        data = response.json()

        # Convert spaces to underscores
        item = item.replace(" ", "_")

        price = data.get(item)

        if price:
            return f"{item.replace('_',' ').title()} average price: KES {price}"
        else:
            return "Sorry, price not found."

    except Exception:
        return "Unable to fetch prices at the moment."

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    msg = request.form.get("Body", "").lower()
    resp = MessagingResponse()

    if "help" in msg:
        resp.message(
            "Household Price Tracker KE\n\n"
            "Available commands:\n"
            "price rice\n"
            "price sugar\n"
            "price cooking oil\n"
            "price salt\n\n"
            "Example:\n"
            "Send: price rice"
        )

    elif "price" in msg:
        item = msg.replace("price", "").strip()
        resp.message(get_price(item))

    else:
        resp.message("Type *help* to see available commands.")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
