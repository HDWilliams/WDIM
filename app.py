from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'It Works'

@app.route('/success')
def success():
    return "Successfully Authenticated, you may now close this tab and return to Slack"

if __name__ == '__main__':
    app.run()