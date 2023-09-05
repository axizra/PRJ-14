import speech_recognition as sr
import pyaudio


r = sr.Recognizer()
with sr.Microphone() as source:
    print("Listening..")
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source)
try:
    print("Recognizing...")
    query = r.recognize_google(audio, language="en-in")
    speech = query.title()
    print(f"USER: {speech}\n")

except Exception:
    print("Did not catch that")
