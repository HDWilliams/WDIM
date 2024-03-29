from flask import Flask, request, jsonify
from slack import WebClient
import requests
import os
import openai
import threading


#environ variables
api_key = os.getenv("api_key")
openai.api_key = os.getenv("openai_key")

#set up slack client sdk
client = WebClient(token=api_key)


def send_slack_message(text, channel_id):
    try: 
        client.chat_postMessage(channel=channel_id, text=text)
    except Exception as e:
        print(f"Error: {e}")

def get_gpt_summary(messages):
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
    return summary

app = Flask(__name__)

def extract_message_text(response):
    messages_text = []
    for item in response['messages']:
        messages_text.append(item['text'])
    return messages_text

def get_channel_history(channel_id):
    response = client.conversations_history(channel=channel_id, limit=100)
    return response

def get_summary_and_send(channel_id):
    history = get_channel_history(channel_id)
    messages = extract_message_text(history)
    summary = get_gpt_summary(messages)
    send_slack_message(summary['choices'][0]['text'], channel_id)


@app.route('/')
def hello_world():
    return 'It Works'

@app.route('/summarize', methods = ['POST'])
def summarize():
    response_url = request.form['response_url']
    channel_id = request.form['channel_id']
    #requests.post(response_url, json={'text': 'Processing...'})

    

    #parse message data, create an array of messages sent in reverse chronological order
    #initial basic implementation to test summary

    summary_thread = threading.Thread(target=get_summary_and_send(channel_id))
    summary_thread.start()
    resp = jsonify(success=True)

    return resp
    


@app.route('/success')
def success():
    return "Successfully Authenticated, you may now close this tab and return to Slack"

if __name__ == '__main__':
    app.run()