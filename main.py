import os
import webbrowser
import requests
import speech_recognition as sr

from gtts import gTTS
from openai import OpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("Enter Your Open AI API Key")
NEWS_API_KEY = os.getenv("Enter Your News API Key")

# Initialize recognizer
recognizer = sr.Recognizer()

# Text-to-Speech function
def speak(text):
    tts = gTTS(text)
    filename = "temp.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

# Function to interact with OpenAI
client = OpenAI(api_key="Enter Your Open AI API Key")
def aiProcess(command):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

# Function to listen for a wake word
def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Listening for 'Jarvis'...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            word = recognizer.recognize_google(audio)
            return word.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("Error with Speech Recognition API")
            return None

# Function to process user commands
def processCommand(command):
    commands = {
        "open google": "https://google.com",
        "open facebook": "https://facebook.com",
        "open youtube": "https://youtube.com",
        "open linkedin": "https://linkedin.com"
    }

    for key in commands:
        if key in command.lower():
            webbrowser.open(commands[key])
            return

    if "news" in command.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}")
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            for article in articles[:5]:  # Limit to 5 news items
                speak(article['title'])
        return
    
    output = aiProcess(command)
    speak(output)

# Main function
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        wake_word = listen_for_wake_word()
        if wake_word == "jarvis":
            speak("Yes?")
            with sr.Microphone() as source:
                print("Listening for command...")
                try:
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
                except sr.UnknownValueError:
                    speak("Sorry, I didn't understand that.")
                except sr.RequestError:
                    speak("There was an error with the speech recognition service.")
