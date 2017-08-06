#app = Flask(__name__)
PAT = 'EAAL4ocStaMQBACk2wMNpXZAUEKtVC6nJxsA4I3xpVCAeLSoacXyiUUZASpzZCT3MCM9ZCulMaVMz2olgEPcvdt8wKPS0EaaQO6ANrhlwA3158OwTZAPbXkuFYKikPzBXOOcdfpZBQ31FZCWg8i1jAMTy4lY2djAZCNfEm59DPzlYawZDZD'

@app.route('/chatbots', methods=['GET'])
def handle_verification():
    print "Handling Verification."
    if request.args.get('hub.verify_token', '') == 'canvip':
        print "Verification successful!"
        return request.args.get('hub.challenge', '')
    else:
        print "Verification failed!"
        return 'Error, wrong validation token'

@app.route('/chatbots', methods=['POST'])
def handle_messages():
    print "Handling Messages"
    payload = request.get_data()
    print payload
    for sender, message in messaging_events(payload):
        print "Incoming from %s: %s" % (sender, message)
        send_message(PAT, sender, message)
    return "ok"

def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.dumps(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"]
        else:
            yield event["sender"]["id"],"xt"
def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient.
    """

    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": token},
        data=json.dumps({
            "recipient": {"id": recipient},
            "message": {"text": text}
        }),
        headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text
