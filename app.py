# app.py
from flask import Flask
from waitress import serve

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask with Waitress!"

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)  # This replaces app.run()
