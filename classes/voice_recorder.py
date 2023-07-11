from utils.constants import *

import pyaudio
import wave
import struct
import math
import time
import sys
import os

class VoiceRecorder:
    @staticmethod
    def rms(frame):
        count = len(frame) / RECORDER_SWIDTH
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)
        sum_squares = 0.0
        for sample in shorts:
            n = sample * RECORDER_SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)
        return rms * 1000
        
    def __init__(self):
        self._rms_threshold = RECORDER_RMS_THRESHOLD
        self._chunk = RECORDER_CHUNK
        self._channels = RECORDER_CHANNELS
        self._format = RECORDER_FORMAT
        self._rate = RECORDER_RATE
        self._timeout_length = RECORDER_TIMEOUT_LENGTH
        self._records_directory = RECORDER_DIRECTORY
        
        self._p = pyaudio.PyAudio()
        self._stream = self._p.open(
            format=self._format,
            frames_per_buffer=self._chunk,
            channels=self._channels,
            rate=self._rate,
            input=RECORDER_INPUT,
        )
        
    def save(self, audio):
        # Create records directory if not exists
        isdir = os.path.isdir(self._records_directory) 
        if not isdir: os.mkdir(self._records_directory)
        
        # Get dynamic filename
        now = time.strftime('%Y-%m-%d-%H-%M-%S')
        n_files = len(os.listdir(self._records_directory))
        filename = os.path.join(self._records_directory, f'{n_files}-{now}.wav')
        
        # Format audio with good parameters
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self._channels)
        wf.setsampwidth(self._p.get_sample_size(self._format))
        wf.setframerate(self._rate)
        wf.writeframes(audio)
        wf.close()
        
        print(f'📁 Record saved at {filename}')
        return filename
        
    def record(self):
        print('🎤 Voice detected !')
        
        audio = []
        now = time.time()
        end = time.time() + self._timeout_length

        while now <= end:
            # Reset timer if the voice is talking
            data = self._stream.read(self._chunk)
            if self.rms(data) >= self._rms_threshold: 
                end = time.time() + self._timeout_length
                
            now = time.time()
            audio.append(data)
            
        audio_path = self.save(b''.join(audio))
        return audio_path

    def listen(self):
        print('👂 Ready to listen')
           
        while True:
            input = self._stream.read(self._chunk)
            rms_value = self.rms(input)
            if rms_value > self._rms_threshold:
                sys.stdout.flush()
                audio = self.record()
                return audio
                break