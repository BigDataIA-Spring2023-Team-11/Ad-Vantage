import os
import openai

openai.api_key = "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"



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


