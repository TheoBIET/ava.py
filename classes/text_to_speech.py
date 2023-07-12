from utils.constants import *
from playsound import playsound
from scipy.io import wavfile
from bark.api import semantic_to_waveform
from bark import generate_audio, SAMPLE_RATE
from bark.generation import (
    generate_text_semantic,
    preload_models,
)

import numpy as np
import nltk
import os
import pyttsx3

os.environ["CUDA_VISIBLE_DEVICES"] = TTS_BARK_CUDA_VISIBLE_DEVICES
os.environ["SUNO_OFFLOAD_CPU"] = TTS_BARK_OFFLOAD_CPU
os.environ["SUNO_USE_SMALL_MODELS"] = TTS_BARK_USE_SMALL_MODELS

class TextToSpeech:
    def __init__(self):
        self._use_local = TTS_USE_LOCAL
        self._lang = TTS_LANGUAGE

        if self._use_local:
            print("🗣️  Loading local Bark AI...")
            preload_models()
            self._bark_speaker = TTS_BARK_SPEAKER
            self._bark_generation_temp = TTS_BARK_GENERATION_TEMP
            self._bark_sample_rate = TTS_BARK_SAMPLE_RATE
            self._bark_min_eos_p = TTS_BARK_MIN_EOS_P
            
        print("🗣️  TTS initialized.")
        
    def speak(self, text):
        if self._use_local:
            self.speak_with_local_ai(text)
        else:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        
    def speak_with_local_ai(self, text):
        sentences = nltk.sent_tokenize(text)
        for i in range(len(sentences)):
            sentence = sentences[i]
            semantic_tokens = generate_text_semantic(
                sentence,
                history_prompt=self._bark_speaker,
                temp=self._bark_generation_temp,
                min_eos_p=self._bark_min_eos_p,
            )
    
            audio_array = semantic_to_waveform(semantic_tokens, history_prompt=self._bark_speaker,)
            int_audio_array = (audio_array * np.iinfo(np.int16).max).astype(np.int16)
            file_name = f'ai/a{i}.wav'
            wavfile.write(file_name, SAMPLE_RATE, int_audio_array)
            playsound(file_name)