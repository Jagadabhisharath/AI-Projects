import openai
import time
from openai import OpenAI
client = OpenAI(api_key="Enter Your Google API Key",
)

def get_completion():
    try:  
      completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
              {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
              {"role": "user", "content": "what is coding"}
              ])
      return completion.choices[0].message.content
    except openai.RateLimitError: 
       print("Rate limit exceeded. Retrying in 10 seconds...")
       time.sleep(10)
       return get_completion

print(get_completion())



