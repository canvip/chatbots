# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,json
import requests
app = Flask(__name__)
#from flask_frozen import Freezer
#from flask_flatpages import FlatPages
#app.config.from_pyfile('settings.py')
#pages = FlatPages(app)
#freezer = Freezer(app)


@app.route('/')
def home():
    return render_template('index.html', )



@app.route('/blog/<path:path>/')
def page(path):
    # Path is the filename of a page, without the file extension
    # e.g. "first-post"
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)


@app.route('/blog/')
def blog():
    posts = [page for page in pages if 'date' in page.meta]
    # Sort pages by date
    sorted_posts = sorted(posts, reverse=True,
        key=lambda page: page.meta['date'])
    return render_template('blog.html', pages=sorted_posts)


##############################################################################################
###############################################
###############################################
#s = u"العربيّة"#
##ASx = s#
#
#json_string = json.dumps(u"احمد").decode('unicode-escape').encode('utf8')
#json.dumps(d).decode('unicode-escape').encode('utf8')
PAT = '#'

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
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
        else:
            yield event["sender"]["id"],text


def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient.
    """

    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": token},
        data=json.dumps({
            "recipient": {"id": recipient},
            "message": {"text": text.encode('utf-8')}
        }),
        headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text



##############################################################################################
###############################################
###############################################

if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=80)
    #main.freezer.freeze()
