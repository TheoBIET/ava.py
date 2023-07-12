"""Core module of the voice assistant."""
from playsound import playsound

from app.classes.speech_recognition import SpeechRecognition
from app.classes.voice_recorder import VoiceRecorder
from app.classes.chatbot import ChatBot
from app.classes.text_to_speech import TextToSpeech

import fake

class VoiceAssistant:
    """Class representing the voice assistant core."""

    def __init__(self):
        self._vr = VoiceRecorder()
        self._sr = SpeechRecognition()
        self._cb = ChatBot()
        self._tts = TextToSpeech()

    def talk_prerecorded(self, file_name):
        """Method that plays a prerecorded voice file."""
        file_path = f'voices/{file_name}.mp3'
        playsound(file_path)

    def run(self):
        """Method that runs the voice assistant and start to listen the user."""
        voice_input_file = self._vr.listen()
        voice_transcription = self._sr.transcribe(voice_input_file)
        print(f'🤫 Whisper transcription: {voice_transcription}')

        if voice_transcription:
            completion = self._cb.chat(voice_transcription)
            if completion:
                print(f'🤖 ChatBot completion: {completion}')
                self._tts.speak(completion)

        self.run()


if __name__ == '__main__':
    va = VoiceAssistant()
    va.talk_prerecorded('how_can_i_help_you')
    va.run()
