import speech_recognition as sr
import pyttsx3
from chatbot import get_chat_response

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)
    except:
        return ""

def voice_chat():
    speak("Loan AI assistant ready")

    while True:
        text = listen()

        if text.lower() in ["exit", "stop"]:
            break

        reply = get_chat_response(text)
        print(reply)
        speak(reply)