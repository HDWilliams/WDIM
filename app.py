from flask import Flask, request, jsonify
from slack import WebClient
import requests
import os

#environ variables
api_key = os.getenv("api_key")

client = WebClient(token=api_key)


app = Flask(__name__)

def extract_message_text(response):
    messages_text = []
    for item in response['messages']:
        messages_text.append(item['text'])
    return messages_text

@app.route('/')
def hello_world():
    return 'It Works'

@app.route('/summarize', methods = ['POST'])
def summarize():
    response_url = request.form['response_url']
    channel_id = request.form['channel_id']
    requests.post(response_url, json={'text': 'Processing...'})

    #get channel history
    response = client.conversations_history(channel=channel_id, limit=100)

    #parese message data, create an array of messages sent in chronological order
    #initial basic implementation to test summary
    messages = extract_message_text(response)
    print(messages)


@app.route('/success')
def success():
    return "Successfully Authenticated, you may now close this tab and return to Slack"

if __name__ == '__main__':
    app.run()