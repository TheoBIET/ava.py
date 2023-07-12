import time
from pyaudio import paInt16
from torch import bfloat16
from bark import SAMPLE_RATE

IS_DEV = True

RECORDER_DIRECTORY = "./records"
RECORDER_SHORT_NORMALIZE = 1.0 / 32768.0
RECORDER_CHUNK = 1024
RECORDER_FORMAT = paInt16
RECORDER_CHANNELS = 2
RECORDER_RATE = 44100
RECORDER_SWIDTH = 2
RECORDER_TIMEOUT_LENGTH = 1
RECORDER_RMS_THRESHOLD = 10
RECORDER_INPUT = True

WHISPER_USE_LOCAL = True
WHISPER_MODEL = "medium"
WHISPER_LANGUAGE = "fr"
WHISPER_DEVICE = "cuda"
WHISPER_FP16 = False if WHISPER_DEVICE == "cpu" else True

OPENAI_API_KEY = "sk-<your key here>"
OPENAI_WHISPER_ENGINE = "whisper-1"
OPENAI_GPT_ENGINE = "gpt-3.5-turbo"
OPENAI_GPT_MAX_TOKENS = 100
OPENAI_LANGUAGE = "fr"

TTS_USE_LOCAL = False
TTS_LANGUAGE = "fr"
TTS_BARK_SPEAKER = "v2/fr_speaker_1"
TTS_BARK_GENERATION_TEMP = 0.6
TTS_BARK_MIN_EOS_P = 0.05
TTS_BARK_SAMPLE_RATE = SAMPLE_RATE
TTS_BARK_CUDA_VISIBLE_DEVICES = "0"
TTS_BARK_OFFLOAD_CPU = "False"
TTS_BARK_USE_SMALL_MODELS = "True"

CHATBOT_USE_LOCAL = False
CHATBOT_MAX_LENGTH = 500
CHATBOT_FALCON_MODEL = "tiiuae/falcon-7b-instruct" if IS_DEV else "tiiuae/falcon-40b-instruct"
CHATBOT_FALCON_PIPELINE_TASK = "text-generation"
CHATBOT_FALCON_CACHE_DIR = "./models/"
CHATBOT_FALCON_TORCH_DTYPE = bfloat16
CHATBOT_FALCON_DEVICE_MAP = "cpu"
CHATBOT_FALCON_OFFLOAD_DIR = "offload"
CHATBOT_FALCON_TOP_K = 10
CHATBOT_FALCON_NUM_RETURN_SEQUENCES = 1
CHATBOT_FALCON_DO_SAMPLE = True
CHATBOT_FALCON_TRUST_REMOTE_CODE = True
CHATBOT_SYSTEM_PROMPT = f"""
Heure : {time.strftime('%H:%M')}
Jour : {time.strftime('%A %d %B %Y')}
"""
CHATBOT_GPT_FUNCTIONS = [
    {
        "name": "launch_a_game",
        "description": "Launch the game by name",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the game, e.g. Trackmania",
                },
            },
            "required": ["name"],
        },
        "keywords": [
            "trackmania",
            "lancer",
            "jeu",
            "game",
            "play",
            "start",
            "launch",
            "open",
            "ouvrir",
            "jouer",
        ],
    },
]
