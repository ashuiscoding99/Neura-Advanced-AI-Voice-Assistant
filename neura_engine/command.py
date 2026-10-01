import pyttsx3
import speech_recognition as sr
import eel
import time

engine = pyttsx3.init('sapi5')
engine.setProperty("rate", 174)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

def speak(text):
    eel.DisplayMessage(text)
    print("Neura:", text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)

    try:
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(1)
        return query.lower()
    except:
        return ""