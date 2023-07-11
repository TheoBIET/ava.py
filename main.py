from classes.speech_recognition import SpeechRecognition
from classes.voice_recorder import VoiceRecorder
from classes.chat_bot import ChatBot
from classes.text_to_speech import TextToSpeech

class VoiceAssistant:
    def __init__(self):
        self._vr = VoiceRecorder()
        self._sr = SpeechRecognition()
        self._cb = ChatBot()
        self._tts = TextToSpeech()
        
    def run(self):
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
    va.run()