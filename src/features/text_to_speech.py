import pyttsx3

def text_to_speech():
    engine = pyttsx3.init()
    text = input("\n🗣️ Enter text to speak: ")
    engine.say(text)
    engine.runAndWait()

