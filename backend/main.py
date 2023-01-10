import os
import tempfile

import whisper
from flask import Flask, jsonify, request
from yt_dlp import YoutubeDL

app = Flask(__name__)
model = whisper.load_model("base")


# Add a get parameter: podcast_url
@app.route('/summarize_podcast', methods=['GET'])
def summarize_podcast():
  print("summarize_podcast")
  podcast_url = request.args.get('podcast_url')
  # check whether podcast_url is not apple podcast nor google podcast
  if "podcasts.apple.com" not in podcast_url and "podcasts.google.com" not in podcast_url:
    # return http 400 with error message
    return jsonify({"error": "podcast_url is not apple podcast"}), 400
  print(f"Downloading podcast from {podcast_url}")
  # create a temp directory using tempfile
  tmp_dir = tempfile.mkdtemp()
  print(f"tmp_dir: {tmp_dir}")

  # use yt-dlp to download the podcast
  ydl_opts = {
    'outtmpl': f'{tmp_dir}/%(title)s.%(ext)s',
  }
  # list all the files in tmp_dir

  with YoutubeDL(ydl_opts) as ydl:
    ydl.download([podcast_url])
    print(f"Downloaded podcast from {podcast_url}")
  file = os.listdir(tmp_dir)[0]
  print("Transcribing using whisper")
  result = model.transcribe(os.path.join(tmp_dir, file))
  print("Transcribed using whisper:")
  print(result["text"])


  return jsonify({'podcast_url': podcast_url})

# run flask app on port 5001
app.run(
  host="localhost",
  port=5001,
  debug=True
)
