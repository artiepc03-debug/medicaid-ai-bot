from flask import Flask, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Medicaid AI Bot is running", 200

@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    resp.say(
        "Welcome to the Medicaid AI assistant. This system is now connected.",
        voice="alice"
    )
    return Response(str(resp), mimetype="text/xml")
