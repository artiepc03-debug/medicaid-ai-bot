from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

sessions = {}

questions = [
    "What is your first name?",
    "What is your last name?",
    "What is your date of birth? Please say month, day, and year.",
    "What is your 5 digit ZIP code?",
    "Are you currently employed, self employed, or not working?"
]

@app.route("/voice", methods=["POST"])
def voice():
    call_sid = request.form.get("CallSid")
    if call_sid not in sessions:
        sessions[call_sid] = {"step": 0, "answers": []}

    step = sessions[call_sid]["step"]
    response = VoiceResponse()

    if step >= len(questions):
        response.say(
            "Thank you. I will prepare your Medicaid application packet for review and signature. "
            "You will receive a text message and email shortly. Goodbye."
        )
        response.hangup()
        return Response(str(response), mimetype="text/xml")

    gather = Gather(
        input="speech",
        action="/process",
        method="POST",
        speech_timeout="auto"
    )
    gather.say(questions[step])
    response.append(gather)
    response.redirect("/voice")
    return Response(str(response), mimetype="text/xml")

@app.route("/process", methods=["POST"])
def process():
    call_sid = request.form.get("CallSid")
    speech = request.form.get("SpeechResult", "")

    if call_sid in sessions:
        sessions[call_sid]["answers"].append(speech)
        sessions[call_sid]["step"] += 1

    response = VoiceResponse()
    response.redirect("/voice")
    return Response(str(response), mimetype="text/xml")

@app.route("/")
def home():
    return "Medicaid AI Bot is running"

if __name__ == "__main__":
    app.run()
