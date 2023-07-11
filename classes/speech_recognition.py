from utils.constants import *
from classes.openai_requester import OpenAI

import whisper

class SpeechRecognition:
    def __init__(self, logger=None):
        self._use_local = WHISPER_USE_LOCAL
        self._lang = WHISPER_LANGUAGE
        
        if self._use_local:
            print(f'🤫 Loading Whisper Model')
            self._options = whisper.DecodingOptions(fp16=WHISPER_FP16, language=self._lang)
            self._model = whisper.load_model(WHISPER_MODEL, device=WHISPER_DEVICE)
        else:
            print(f'🤫 Loading Whisper API')
            self._openai = OpenAI()

    def transcribe(self, file):
        if self._use_local: return self._model.transcribe(file, language=self._lang)['text']
        else: return self._openai.transcribe(file)
        return transcription