from dotenv import load_dotenv

import gpt

load_dotenv()

import os
import tempfile
import whisper
from flask import Flask, jsonify, request
from flask_cors import CORS
from yt_dlp import YoutubeDL
import logging
from test import TEST_PODCAST_SCRIBE
import shutil

OPENAI_KEY = os.environ.get("OPENAI_KEY")

logging.basicConfig(
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.INFO,
  datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
CORS(app)

model = whisper.load_model("base")


def get_whisper_transcript(file_path):
  logging.info(f"Transcribing {file_path} using whisper")
  result = model.transcribe(file_path)
  logging.info(f"Successfully transcribed {file_path} using whisper")
  return result["text"]


@app.route('/test', methods=['GET'])
def test():
  return jsonify({"message": "Hello World!"})

@app.route('/summarize_podcast', methods=['GET'])
def summarize_podcast():
  logging.info("summarize_podcast")
  podcast_url = request.args.get('podcast_url')
  # check whether podcast_url is not apple podcast nor google podcast
  if "podcasts.apple.com" not in podcast_url and "podcasts.google.com" not in podcast_url:
    # return http 400 with error message
    return jsonify({"error": "podcast_url is not apple podcast"}), 400
  logging.info(f"Downloading podcast from {podcast_url}")
  # create a temp directory using tempfile
  tmp_dir = tempfile.mkdtemp()
  logging.info(f"tmp_dir: {tmp_dir}")

  # use yt-dlp to download the podcast
  ydl_opts = {
    'outtmpl': f'{tmp_dir}/%(title)s.%(ext)s',
  }
  # list all the files in tmp_dir

  with YoutubeDL(ydl_opts) as ydl:
    ydl.download([podcast_url])
    logging.info(f"Downloaded podcast from {podcast_url}")
  file = os.listdir(tmp_dir)[0]
  podcast_title = file.split(".")[0]
  transcript = get_whisper_transcript(os.path.join(tmp_dir, file))
  # delete tmp_dir directory
  shutil.rmtree(tmp_dir)
  summary = gpt.summarize_podcast(podcast_title, transcript)
  return jsonify({'podcast_url': podcast_url, 'summary': summary, 'podcast_title': podcast_title})


logging.info("Starting the app")
# run flask app on port 5001
app.run(
  host="0.0.0.0",
  port=5001,
  debug=True
)
