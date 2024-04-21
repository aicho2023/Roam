from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

FB_ACCESS_TOKEN = 'EAALiBWhjZBIwBO2QxtXPQGLRACkvjV457egwR8SU9pnv1htDJnxLeIty0yGgXZCvU6fiPCCRQ0vsc42nZAjHKQIxMSPAu3FkUQrDmXC1lLJRZCBNKNTkSeEFjv1YrZBboi0XEWpJGEM3rsJQOOa3RGBknuXX2ckwCqsJ8yaRfTjSU1uKOg3kaZBJZA0vZAWqSk43L3h7ZAk87uAZDZD'
VERIFY_TOKEN = 'alfred'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                return challenge
            else:
                return 'Verification token mismatch', 403
    else:
        data = request.json
        messaging_event = data['entry'][0]['messaging'][0]
        sender_id = messaging_event['sender']['id']
        message = messaging_event.get('message')

        if message and 'text' in message:
            text = message['text']
            send_message(sender_id, text)
        return 'OK'

def send_message(recipient_id, text):
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'messaging_type': 'RESPONSE',
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'text': text
        }
    }
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + FB_ACCESS_TOKEN
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())

if __name__ == '__main__':
    # Ensure it listens on all network interfaces, not just the local host
    app.run(host='0.0.0.0', port=8080, debug=True)
