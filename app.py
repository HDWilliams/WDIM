from flask import Flask, request, jsonify
from slack import WebClient
import requests
import os
import openai


#environ variables
api_key = os.getenv("api_key")
openai.api_key = os.getenv("openai_key")

#set up slack client sdk
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

    #parse message data, create an array of messages sent in reverse chronological order
    #initial basic implementation to test summary
    messages = extract_message_text(response)
    
    #send messages as a string to openai api for summary
    prompt_text = ", ".join(messages)
    prompt_action = "\n\nThe text is a comma seperated list of messages in a slack channel in reverse chronological order. Give a Tl;dr"
    prompt = prompt_text + prompt_action
    summary = openai.Completion.create(
        model = "text-davinci-003", 
        prompt = prompt_text + prompt_action,
        temperature=1,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1
    )

    print(summary)

    resp = jsonify(success=True)

    return resp
    


@app.route('/success')
def success():
    return "Successfully Authenticated, you may now close this tab and return to Slack"

if __name__ == '__main__':
    app.run()