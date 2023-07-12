"""Voice Recorder configuration file."""
from pyaudio import paInt16
from app.utils.get_env import get_env

RECORDER = {
    "FORMAT": paInt16,
    "SHORT_NORMALIZE": 1.0 / 32768.0,
    "DIRECTORY": get_env("RECORDER_DIRECTORY", str),
    "CHUNK": get_env("RECORDER_CHUNK", int),
    "CHANNELS": get_env("RECORDER_CHANNELS", int),
    "RATE": get_env("RECORDER_RATE", int),
    "SWIDTH": get_env("RECORDER_SWIDTH", int),
    "TIMEOUT_LENGTH": get_env("RECORDER_TIMEOUT_LENGTH", int),
    "RMS_THRESHOLD": get_env("RECORDER_RMS_THRESHOLD", int),
    "INPUT": get_env("RECORDER_INPUT", bool),
}
