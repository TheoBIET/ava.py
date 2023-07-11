from utils.constants import *
import pyttsx3

class TextToSpeech:
    def __init__(self):
        self._use_local = TTS_USE_LOCAL
        self._use_ai = TTS_USE_AI
        self._lang = TTS_LANGUAGE
        
    def speak(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()