"""Class representing the voice assistant core."""
from app.classes.speech_recognition import SpeechRecognition
from app.classes.voice_recorder import VoiceRecorder
from app.classes.chatbot import ChatBot
from app.classes.text_to_speech import TextToSpeech

class VoiceAssistant:
    """Class representing the voice assistant core."""
    def __init__(self):
        self._vr = VoiceRecorder()
        self._sr = SpeechRecognition()
        self._cb = ChatBot()
        self._tts = TextToSpeech()

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

