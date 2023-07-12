"""Chatbot configuration file."""
from torch import bfloat16
from app.utils.get_env import get_env

CHATBOT = {
    "USE_LOCAL": get_env("CHATBOT_USE_LOCAL", bool),
    "MAX_LENGTH": get_env("CHATBOT_MAX_LENGTH", int),
    "LOCAL": {
        "MODEL": get_env("CHATBOT_LOCAL_MODEL", str),
        "PIPELINE": get_env("CHATBOT_LOCAL_PIPELINE", str),
        "CACHE_DIR": get_env("CHATBOT_LOCAL_CACHE_DIR", str),
        "DEVICE_MAP": get_env("CHATBOT_LOCAL_DEVICE_MAP", str),
        "TOP_K": get_env("CHATBOT_LOCAL_TOP_K", int),
        "NUM_RETURN_SEQUENCES": get_env("CHATBOT_LOCAL_NUM_RETURN_SEQUENCES", int),
        "DO_SAMPLE": get_env("CHATBOT_LOCAL_DO_SAMPLE", bool),
        "TRUST_REMOTE_CODE": get_env("CHATBOT_LOCAL_TRUST_REMOTE_CODE", bool),
        "TORCH_DTYPE": bfloat16,
    }
}
