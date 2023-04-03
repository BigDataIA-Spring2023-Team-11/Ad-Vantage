import os
import openai
import requests




def get_grammer_corrected_text(input_text):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Correct this to standard English:\n\n{input_text}",
    temperature=0,
    max_tokens=200,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )

  # Extract the generated text from the API response
  grammer_corrected_text = response.choices[0].text
  return grammer_corrected_text


def keyword_generator(input_text):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Extract keywords from this text:\n\n{input_text}",
    temperature=0.5,
    max_tokens=200,
    top_p=1.0,
    frequency_penalty=0.8,
    presence_penalty=0.0
  )
  keywords = response.choices[0].text
  return keywords

def product_name_generator(product_description, seed_words):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Product description: {product_description}\nSeed words: {seed_words}",
    temperature=0.8,
    max_tokens=60,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )
  products_names = response.choices[0].text
  return products_names


def get_answers1():
  responses = []
  questions = ["Can you summarize what the speaker said?", "What was the main point of the conversation?", "Was there anything surprising or unexpected in the conversation?"]
  for q in questions:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are filling out a questionnaire."},
        {"role": "user", "content": q}
      ]
    )
    answer = response.choices[0].text.strip()
    responses.append(answer)

  return responses


def get_answers():
  responses = []
  questions = ["Can you summarize what the speaker said?",
               "What was the main point of the conversation?",
               "Was there anything surprising or unexpected in the conversation?"]

  # transcript = "Speaker 1: Hi, how are you?\nSpeaker 2: I'm good, thanks for asking. How about you?\nSpeaker 1: I'm doing well, thanks. So, what brings you here today?"
  transcript = "on the work, scraping on the data science, whatever you're web scraping for, you can focus on that. They have a success rate of average 99.2% and the residential proxies offer, as I said, 100 million plus legit IPs from 195 countries. You can also take a look at their quick start. You can use this with curl with a command line tool on Linux on Windows. You can use it for PHP and probably most interesting for you guys, you can use it with Python as well. You can look at the tutorial here to see how it's done. You can specify a server. You can also specify the country, the city. You can do all this manually and these are legitimate IP addresses, reliable service. The company is very reliable. If you go to Reddit and you look for best proxy server."
  for q in questions:
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=f"{transcript}\nQ: {q}\nA:",
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.7,
    )

    answer = response.choices[0].text.strip()
    responses.append(answer)

  return responses

# def ques():
#
#   # Set up API endpoint and headers
#   endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"
#   headers = {
#       "Content-Type": "application/json",
#       "Authorization": f"Bearer {openai.api_key}",
#   }
#
#   # Set up transcripted text prompt
#   transcript = """Transcript: Speaker 1: Hi, how are you?
#   Speaker 2: I'm good, thanks for asking. How about you?
#   Speaker 1: I'm doing well, thanks. So, what brings you here today?"""
#   prompt = f"Please complete the following questionnaire:\n\n1. Can you summarize what the speaker said?\n2. What was the main point of the conversation?\n3. Was there anything surprising or unexpected in the conversation?\n\nTranscript: {transcript}"
#
#   # Set up data payload
#   data = {
#       "prompt": prompt,
#       "temperature": 0.5,
#       "max_tokens": 500,
#       "stop": "\n\n"
#   }
#
#   # Send request to API
#   response = requests.post(endpoint, headers=headers, json=data)
#
#   # Get response text
#   response_text = response.json()
#
#   # Print response
#   return response_text
