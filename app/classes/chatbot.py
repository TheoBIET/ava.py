"""Class used to chat with the user."""
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM

from app.classes.openai_requester import OpenAI
from app.config.chatbot import CHATBOT

class ChatBot:          # pylint: disable=too-few-public-methods
    """Class used to chat with the user."""
    def __init__(self):
        self._use_local = CHATBOT['USE_LOCAL']
        self._max_length = CHATBOT['MAX_LENGTH']

        if self._use_local:
            self._initialize_local()
        else:
            self._openai = OpenAI()
            print('🤖 Using OpenAI ChatBot')

    def chat(self, content):
        """Get a response from the chatbot."""
        if self._use_local:
            return self._get_sequence(content)

        return self._openai.chat(content, max_tokens=self._max_length)

    def _get_sequence(self, content):
        sequences = self._pipeline(
            content,
            eos_token_id=self._tokenizer.eos_token_id
        )

        for seque in sequences:
            print(f"Result: {seque['generated_text']}")

        return sequences[0]['generated_text']

    def _initialize_local(self):
        used_model = CHATBOT['LOCAL']['MODEL']
        print(f'🤖 Using Falcon ChatBot ({used_model})')

        self._tokenizer = AutoTokenizer.from_pretrained(
            used_model,
            cache_dir=CHATBOT['LOCAL']['CACHE_DIR']
        )

        self._model = AutoModelForCausalLM.from_pretrained(
            used_model,
            cache_dir=CHATBOT['LOCAL']['CACHE_DIR'],
            torch_dtype=CHATBOT['LOCAL']['TORCH_DTYPE'],
            trust_remote_code=CHATBOT['LOCAL']['TRUST_REMOTE_CODE'],
            device_map=CHATBOT['LOCAL']['DEVICE_MAP'],
        )

        self._pipeline = transformers.pipeline(
            CHATBOT['LOCAL']['PIPELINE'],
            model=self._model,
            tokenizer=self._tokenizer,
            max_length=self._max_length,
            device_map=CHATBOT['LOCAL']['DEVICE_MAP'],
            do_sample=CHATBOT['LOCAL']['DO_SAMPLE'],
            top_k=CHATBOT['LOCAL']['TOP_K'],
            num_return_sequences=CHATBOT['LOCAL']['NUM_RETURN_SEQUENCES'],
            eos_token_id=self._tokenizer.eos_token_id
        )
