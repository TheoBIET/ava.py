"""Class used to interact with OpenAI API."""
import json
import dataclasses
import openai

from app.config.openai import OPENAI
from app.config.chatbot import CHATBOT
from app.classes.chatbot_functions import ChatBotFunctions

@dataclasses.dataclass
class OpenAIConfig:
    """Class used to store the openai configuration."""
    language: str
    whisper_engine: str
    gpt_engine: str
    gpt_max_tokens: int
    functions: list
    gpt_roles: dict
    gpt_conversation: list


class OpenAI:
    """Class used to interact with OpenAI API."""
    def __init__(self):
        self._openai = openai
        self._openai.api_key = OPENAI['API_KEY']
        self._config = OpenAIConfig(
            language = OPENAI['LANGUAGE'],
            whisper_engine = OPENAI['WHISPER']['ENGINE'],
            gpt_engine = OPENAI['GPT']['ENGINE'],
            gpt_max_tokens = CHATBOT['MAX_LENGTH'],
            functions = OPENAI['GPT']['FUNCTIONS'],
            gpt_roles = OPENAI['GPT']['ROLES'],
            gpt_conversation = [{
                "role": OPENAI['GPT']['ROLES']['system'],
                "content": OPENAI['GPT']['SYSTEM_PROMPT']
            }]
        )

        print('🤖 OpenAI is ready !')

    def transcribe(self, file):
        """Transcribe an audio file to text using whisper openai api."""
        with open(file, 'rb') as audio_file:
            response = openai.Audio.transcribe(
                model=self._config.whisper_engine,
                language=self._config.language,
                file=audio_file,
            )

            return response['text']

    def _add(self, role, content):
        """Add a message to the conversation list."""
        self._config.gpt_conversation.append({
            "role": role,
            "content": content
        })

    def _clear(self):
        """Clear the conversation list."""
        self._config.gpt_conversation = []

    def chat(self, content, max_tokens=None):
        """Get a chat completion from gpt openai api."""
        self._add(self._config.gpt_roles['user'], content)

        response = openai.ChatCompletion.create(
            model=self._config.gpt_engine,
            messages=self._config.gpt_conversation,
            max_tokens=max_tokens if max_tokens else self._config.gpt_max_tokens,
            functions=self._config.functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )

        function_name = None
        message = response['choices'][0]['message']
        self._add(message['role'], message['content'])

        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            available_functions = ChatBotFunctions.get_availables_functions()
            if function_name in available_functions:
                function = available_functions[function_name]
                args = json.loads(message["function_call"]["arguments"])
                args_str = ", ".join([f"{k}='{v}'" for k, v in args.items()])
                print(f"🤖 Calling function {function_name}({args_str})")
                function(**args)

        return message['content']
