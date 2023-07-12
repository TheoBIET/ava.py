"""Module used to record the user voice."""
import wave
import struct
import math
import time
import sys
import os
import dataclasses
import pyaudio

from app.config.recorder import RECORDER

@dataclasses.dataclass
class VoiceRecorderConfig:
    """Class used to store the voice recorder configuration."""
    rms_threshold: int
    chunk: int
    channels: int
    format: int
    rate: int
    timeout_length: int
    records_directory: str

class VoiceRecorder:
    """Class used to record the user voice."""
    @staticmethod
    def rms(frame):
        """Returns the root mean square of the frame."""
        count = len(frame) / RECORDER['SWIDTH']
        sformat = f'{int(count)}h'
        shorts = struct.unpack(sformat, frame)
        sum_squares = 0.0
        for sample in shorts:
            n_samples = sample * RECORDER['SHORT_NORMALIZE']
            sum_squares += n_samples * n_samples
        rms = math.pow(sum_squares / count, 0.5)
        return rms * 1000

    def __init__(self):
        self._config = VoiceRecorderConfig(
            rms_threshold = RECORDER['RMS_THRESHOLD'],
            chunk = RECORDER['CHUNK'],
            channels = RECORDER['CHANNELS'],
            format = RECORDER['FORMAT'],
            rate = RECORDER['RATE'],
            timeout_length = RECORDER['TIMEOUT_LENGTH'],
            records_directory = RECORDER['DIRECTORY'],
        )

        self._p = pyaudio.PyAudio()
        self._stream = self._p.open(
            format=self._config.format,
            frames_per_buffer=self._config.chunk,
            channels=self._config.channels,
            rate=self._config.rate,
            input=RECORDER['INPUT'],
        )

    def save(self, audio):
        """Save the audio into a wav file."""
        # Create records directory if not exists
        if not os.path.isdir(self._config.records_directory):
            os.mkdir(self._config.records_directory)

        # Get dynamic filename
        now = time.strftime('%Y-%m-%d-%H-%M-%S')
        n_files = len(os.listdir(self._config.records_directory))
        filename = os.path.join(self._config.records_directory, f'{n_files}-{now}.wav')

        # Format audio with good parameters
        w_file = wave.open(filename, 'wb')
        w_file.setnchannels(self._config.channels)
        w_file.setsampwidth(self._p.get_sample_size(self._config.format))
        w_file.setframerate(self._config.rate)
        w_file.writeframes(audio)
        w_file.close()

        print(f'📁 Record saved at {filename}')
        return filename

    def record(self):
        """Record the user voice when he talk, then save it and return the path."""
        print('🎤 Voice detected !')

        audio = []
        now = time.time()
        end = time.time() + self._config.timeout_length

        while now <= end:
            # Reset timer if the voice is talking
            data = self._stream.read(self._config.chunk)
            if self.rms(data) >= self._config.rms_threshold:
                end = time.time() + self._config.timeout_length

            now = time.time()
            audio.append(data)

        audio_path = self.save(b''.join(audio))
        return audio_path

    def listen(self):
        """Loop that listens the user in real time and record the voice when detected."""
        print('👂 Ready to listen')
        while True:
            sinput = self._stream.read(self._config.chunk)
            rms_value = self.rms(sinput)
            if rms_value > self._config.rms_threshold:
                sys.stdout.flush()
                audio = self.record()
                return audio
