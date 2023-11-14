from flask import Flask

app = Flask(__name__)

@app.route('/')
def is_running():
    return 'API is running go to documentation'
