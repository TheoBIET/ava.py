"""TTS configuration file."""
from bark import SAMPLE_RATE
from app.utils.get_env import get_env

TTS = {
    "USE_LOCAL": get_env("TTS_USE_LOCAL", bool),
    "LANGUAGE": get_env("TTS_LANGUAGE", str),
    "LOCAL": {
        "SAMPLE_RATE": SAMPLE_RATE,
        "SPEAKER": get_env("TTS_LOCAL_SPEAKER", str),
        "GENERATION_TEMP": get_env("TTS_LOCAL_GENERATION_TEMP", float),
        "MIN_EOS_P": get_env("TTS_LOCAL_MIN_EOS_P", float),
        "CUDA_VISIBLE_DEVICES": get_env("TTS_LOCAL_CUDA_VISIBLE_DEVICES", str),
        "OFFLOAD_CPU": get_env("TTS_LOCAL_OFFLOAD_CPU", str), # need str for os.environ
        "USE_SMALL_MODELS": get_env("TTS_LOCAL_USE_SMALL_MODELS", str), # need str for os.environ
    }
}
