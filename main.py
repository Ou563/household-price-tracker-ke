from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json
import os

app = Flask(__name__)

# Household items list
HOUSEHOLD_ITEMS = [
    "salt", "sugar", "cooking_oil", "rice", "maize_flour", "milk", "soap",
    "matches", "eggs", "tea", "bread", "vegetable_oil", "bread_rolls",
    "beans", "water", "porridge_flour", "cooking_salt", "soda", "soap_powder"
]

# Path to your local JSON prices
LOCAL_JSON = "prices.json"

def get_price(item):
    item = item.lower().replace(" ", "_")

    # Read local JSON
    try:
        with open(LOCAL_JSON) as f:
            data = json.load(f)
        if item in data:
            return f"{item.replace('_',' ').title()} price: KES {data[item]}"
    except Exception as e:
        print("Error reading prices.json:", e)
        return "Unable to fetch prices at the moment."

    return "Sorry, price not found."

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    msg = request.form.get("Body", "").lower()
    resp = MessagingResponse()

    if "help" in msg:
        help_text = "Household Price Tracker KE\n\nAvailable commands:\n"
        for item in HOUSEHOLD_ITEMS:
            help_text += f"price {item}\n"
        help_text += "\nExample:\nSend: price rice"
        resp.message(help_text)

    elif "price" in msg:
        item = msg.replace("price", "").strip()
        resp.message(get_price(item))

    else:
        resp.message("Type *help* to see available commands.")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
