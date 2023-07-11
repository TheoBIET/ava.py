from utils.constants import *
import openai
import json
import sys
import subprocess

def launch_a_game(name):
    name = name.lower()
    
    path = {
        'trackmania': 'E:\SteamLibrary\steamapps\common\Trackmania\Trackmania.exe',
    }
    
    subprocess.Popen(path[name])
    
available_functions = {
    'launch_a_game': launch_a_game,
}

class OpenAI:
    def __init__(self):
        # Whisper Configuration
        self._whisper_engine = OPENAI_WHISPER_ENGINE
        # GPT Configuration
        self._gpt_engine = OPENAI_GPT_ENGINE
        self._gpt_max_tokens = OPENAI_GPT_MAX_TOKENS
        self._functions = CHATBOT_GPT_FUNCTIONS
        self._gpt_roles = {
            'user': 'user',
            'assistant': 'assistant',
            'system': 'system',
            'function': 'function'
        }
        
        self._gpt_conversation = [{
            "role": self._gpt_roles['system'],
            "content": CHATBOT_SYSTEM_PROMPT
        }]
        
        self._language = OPENAI_LANGUAGE
        self._openai = openai
        self._openai.api_key = OPENAI_API_KEY
        
        # Test OpenAI API Key
        try: self._openai.Engine.retrieve(self._whisper_engine)
        except Exception as e:
            print(f'🤖 OpenAI API Key is not valid !')
            sys.exit(1)
            
        print(f'🤖 OpenAI is ready !')        
        
    def transcribe(self, file):
        audio_file = open(file, 'rb')
        response = openai.Audio.transcribe(
            model=self._whisper_engine,
            file=audio_file,
            language=self._language
        )
        
        return response['text']
    
    def _add(self, role, input):
        self._gpt_conversation.append({
            "role": role,
            "content": input
        })
        
    def _clear(self):
        self._gpt_conversation = []
    
    def chat(self, input, max_tokens=None):
        self._add(self._gpt_roles['user'], input)
                
        response = openai.ChatCompletion.create(
            model=self._gpt_engine,
            messages=self._gpt_conversation,
            max_tokens=max_tokens if max_tokens else self._gpt_max_tokens,
            functions=self._functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        
        function_name = None
        message = response['choices'][0]['message']
        self._add(message['role'], message['content'])
        
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            if function_name in available_functions:
                function = available_functions[function_name]
                args = json.loads(message["function_call"]["arguments"])
                args_str = ", ".join([f"{k}='{v}'" for k, v in args.items()])
                print(f'🤖 ChatBot call function: {function_name}({args_str})')
                function(**args)
        
        return message['content']