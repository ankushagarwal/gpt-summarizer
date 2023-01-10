import requests


def main():
  # send a get request to localhost:5000/summarize_podcast with a get parameter podcast_url which is url encoded
  podcast_url = "https://podcasts.apple.com/us/podcast/207-whitney-webb-returns/id1135137367?i=1000482637777"
  print(f"podcast_url: {podcast_url}")
  url = "http://localhost:5001/summarize_podcast"
  response = requests.get(url, params={"podcast_url": podcast_url})
  print(response.status_code)


if __name__ == '__main__':
  main()
