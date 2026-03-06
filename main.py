from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    # Get the incoming message text
    msg = request.form.get("Body", "").lower()
    resp = MessagingResponse()

    # Help menu
    if "help" in msg:
        resp.message(
            "🇰🇪 Household Price Tracker KE\n\n"
            "Available commands:\n"
            "price rice\n"
            "price sugar\n"
            "price cooking oil\n"
            "price salt\n\n"
            "Example:\n"
            "Send: price rice"
        )

    # Price commands
    elif "price rice" in msg:
        resp.message("Rice average price in Kenya: KSh 180 per 2kg")
    elif "price sugar" in msg:
        resp.message("Sugar average price in Kenya: KSh 200 per 2kg")
    elif "price cooking oil" in msg:
        resp.message("Cooking oil average price: KSh 350 per litre")
    elif "price salt" in msg:
        resp.message("Salt average price in Kenya: KSh 50 per 1kg")

    # Default response for unknown messages
    else:
        resp.message("Type *help* to see available commands.")

    return str(resp)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
