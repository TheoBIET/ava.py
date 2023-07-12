"""Whisper configuration file (Speech Recognition)."""
from app.utils.get_env import get_env

SPEECH_RECOGNITION = {
    "USE_LOCAL": get_env("SPEECH_RECOGNITION_USE_LOCAL", bool),
    "LANGUAGE": get_env("SPEECH_RECOGNITION_LANGUAGE", str),
    "LOCAL": {
        "MODEL": get_env("SPEECH_RECOGNITION_LOCAL_MODEL", str),
        "DEVICE": get_env("SPEECH_RECOGNITION_LOCAL_DEVICE", str),
        "FP16": get_env("SPEECH_RECOGNITION_LOCAL_DEVICE", str) != "cpu",
    }
}
