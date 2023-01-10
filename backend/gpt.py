import openai
import logging

openai.api_key = os.environ.get("OPENAI_KEY")

def summarize_section(podcast_title, text):
    prompt = f"""
You are a brilliant podcast summarizer. You are given the following section from a podcast titled "{podcast_title}".
Please give me 4 most important key ideas the host and guests are trying to communicate in this section.
For each key idea please provide a list of arguments and examples they use to convey the idea.
Make sure to avoid repeating yourself.
The summary should be in a markdown numbered list and sublist format.
Here is the section within triple angle brackets : <<< {text} >>>
Key Ideas:

"""
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0,
        best_of=1
    )

    message = completions.choices[0].text
    return message

def summarize_podcast(podcast_title, text, max_words_per_section=2000):
  logging.info(f"Summarizing podcast {podcast_title}")
  # split the text into a list of words
  words = text.split()
  # initialize a list to store the chunks
  chunks = []
  # initialize a counter for the number of words in the current chunk
  count = 0
  # initialize a string to store the current chunk
  chunk = ''
  # iterate over the words
  for word in words:
    # add the word to the current chunk
    chunk += word + ' '
    # increment the word count
    count += 1
    # if the word count has reached the maximum, append the current chunk to the list of chunks and reset the count and chunk
    if count == max_words_per_section:
      chunks.append(chunk)
      count = 0
      chunk = ''
  # append the remaining chunk to the list of chunks
  chunks.append(chunk)
  # go over the chunks and print them

  logging.info(f"Split the podcast into {len(chunks)} sections")
  result = "AI Summary\n"
  for i, chunk in enumerate(chunks):
    result += f"Part {i+1}/{len(chunks)}:\n"
    result += "Summary (Key-ideas in this section): \n"
    result += summarize_section(podcast_title, chunk)
    result += "\n--------\n"
    logging.info(f"Finished summarizing part {i+1}/{len(chunks)}")
  return result
