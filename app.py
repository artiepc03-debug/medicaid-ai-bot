from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Medicaid AI Bot is running"

@app.route("/intake", methods=["POST"])
def intake():
    data = request.get_json(silent=True) or {}

    required_fields = [
        "name",
        "dob",
        "county",
        "household_size",
        "monthly_income",
        "single_adult"
    ]

    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    # NC Medicaid Expansion (single adult) - simple placeholder threshold
    income_limit = 1677 # approx monthly limit, update later with exact FPL logic

    try:
        monthly_income = int(float(data["monthly_income"]))
        household_size = int(data["household_size"])
        single_adult = bool(data["single_adult"])
    except Exception:
        return jsonify({"error": "Invalid data types. Use numbers for income/household_size and true/false for single_adult."}), 400

    eligible = (single_adult is True and household_size == 1 and monthly_income <= income_limit)

    return jsonify({
        "eligible": eligible,
        "program": "NC Medicaid Expansion",
        "next_step": "Proceed with Medicaid application" if eligible else "Review ACA or other coverage options"
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
from flask import Flask, request, jsonify
from twilio.twiml.voice_response import VoiceResponse
import os

# existing app = Flask(__name__) stays

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    response.say(
        "Welcome to the Medicaid AI assistant. I will ask you a few questions to check eligibility.",
        voice="alice"
    )
    response.say(
        "For now, this system is under testing. Please check back shortly.",
        voice="alice"
    )
    return str(response)
