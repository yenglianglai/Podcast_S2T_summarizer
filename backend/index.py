from flask import Flask, request
from flask_cors import CORS
from transcribe import download_podcast, transcribe_long
import logging

logging.basicConfig(filename="myapp.log", level=logging.INFO)

app = Flask("app")
CORS(app)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/transcribe")
def transcribe():
    url = request.args.get("url")
    download_podcast.download_mp3(url)
    transcript = transcribe_long.transcribe_local_mp3("audio.mp3")
    return {"transcribed": transcript}


@app.route("/summarize")
def summarize():
    content = request.args.get("content")
    print(content)
    return {"summarized": "Ya Hi"}


app.run(port=4000, debug=True)
