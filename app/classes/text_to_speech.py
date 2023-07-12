"""Class used to speak to the user."""
import os
import time
import numpy as np
import nltk
import pyttsx3
from scipy.io import wavfile
from bark.api import semantic_to_waveform
from bark.generation import (
    generate_text_semantic,
    preload_models,
)

from app.config.tts import TTS
from app.utils.talk_wav import talk_wav

os.environ["CUDA_VISIBLE_DEVICES"] = TTS["LOCAL"]["CUDA_VISIBLE_DEVICES"]
os.environ["SUNO_OFFLOAD_CPU"] = TTS["LOCAL"]["OFFLOAD_CPU"]
os.environ["SUNO_USE_SMALL_MODELS"] = TTS["LOCAL"]["USE_SMALL_MODELS"]


class TextToSpeech:
    """Class used to speak to the user."""
    def __init__(self):
        self._use_local = TTS["USE_LOCAL"]
        self._lang = TTS["LANGUAGE"]

        if self._use_local:
            print("🗣️  Loading local Bark AI...")
            preload_models()
            self._local_speaker = TTS["LOCAL"]["SPEAKER"]
            self._local_generation_temp = TTS["LOCAL"]["GENERATION_TEMP"]
            self._local_sample_rate = TTS["LOCAL"]["SAMPLE_RATE"]
            self._local_min_eos_p = TTS["LOCAL"]["MIN_EOS_P"]

        print("🗣️  TTS initialized.")

    def speak(self, text):
        """Speak the text to the user."""
        if self._use_local:
            self.speak_with_local_ai(text)
        else:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

    def speak_with_local_ai(self, text):
        """Generate an audio file from text using Bark AI."""
        sentences = nltk.sent_tokenize(text)
        for sentence in enumerate(sentences):
            sentence = sentence[1]
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            semantic_tokens = generate_text_semantic(
                sentence,
                history_prompt=self._local_speaker,
                temp=self._local_generation_temp,
                min_eos_p=self._local_min_eos_p,
            )

            audio_array = semantic_to_waveform(semantic_tokens, history_prompt=self._local_speaker,)
            int_audio_array = (audio_array * np.iinfo(np.int16).max).astype(np.int16)
            os_path = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
            file_name = f"{timestamp}.wav"
            file_path = os_path + f'/../../voices/{file_name}'

            wavfile.write(file_path, self._local_sample_rate, int_audio_array)
            talk_wav(file_name)
