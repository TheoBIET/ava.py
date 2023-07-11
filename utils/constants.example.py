import pyaudio
import time

IS_DEV = True

RECORDER_DIRECTORY = "./records"
RECORDER_SHORT_NORMALIZE = 1.0 / 32768.0
RECORDER_CHUNK = 1024
RECORDER_FORMAT = pyaudio.paInt16
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

TTS_USE_AI = False
TTS_USE_LOCAL = False if not TTS_USE_AI else not IS_DEV
TTS_LANGUAGE = "fr"

CHATBOT_USE_LOCAL = False
CHATBOT_MAX_LENGTH = 500
CHATBOT_LOCAL_MODEL = (
    "tiiuae/falcon-7b-instruct" if IS_DEV else "tiiuae/falcon-40b-instruct"
)
CHATBOT_LOCAL_PIPELINE_TASK = "text-generation"
CHATBOT_LOCAL_CACHE_DIR = "./models/"
CHATBOT_SYSTEM_PROMPT = f"""
<your system prompt here>
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