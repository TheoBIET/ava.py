from utils.constants import *
from classes.openai_requester import OpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

class ChatBot:
    def __init__(self):
        self._use_local = CHATBOT_USE_LOCAL
        self._max_length = CHATBOT_MAX_LENGTH
        
        if self._use_local:
            self._local_model = CHATBOT_FALCON_MODEL
            self._pipeline_task = CHATBOT_FALCON_PIPELINE_TASK
            self._cache_dir = CHATBOT_FALCON_CACHE_DIR
            self._torch_dtype = CHATBOT_FALCON_TORCH_DTYPE
            self._trust_remote_code = CHATBOT_FALCON_TRUST_REMOTE_CODE
            self._device_map = CHATBOT_FALCON_DEVICE_MAP
            self._offload_dir = CHATBOT_FALCON_OFFLOAD_DIR
            self._do_sample = CHATBOT_FALCON_DO_SAMPLE
            self._top_k = CHATBOT_FALCON_TOP_K
            self._num_return_sequences = CHATBOT_FALCON_NUM_RETURN_SEQUENCES
            self._initializeLocal()
            print(f'🤖 Using Falcon ChatBot ({self._local_model})')
        else:
            self._openai = OpenAI()
            print(f'🤖 Using OpenAI ChatBot')
    
    def chat(self, input):
        if self._use_local: return self._getSequence(input)
        else: return self._openai.chat(input, max_tokens=self._max_length)
    
    def _getSequence(self, input):
        sequences = self._pipeline(
            input,
            eos_token_id=self._tokenizer.eos_token_id,
        )
        
        for seq in sequences:
            print(f"Result: {seq['generated_text']}")
        
        return sequences[0]['generated_text']
    
    def _initializeLocal(self):
        self._tokenizer = AutoTokenizer.from_pretrained(
            self._local_model,
            cache_dir=self._cache_dir
        )

        self._model = AutoModelForCausalLM.from_pretrained(
            self._local_model,
            cache_dir=self._cache_dir, 
            torch_dtype=torch.bfloat16,
            trust_remote_code=self._trust_remote_code,
            device_map=self._device_map,
            offload_folder=self._offload_dir
        )

        self._pipeline = transformers.pipeline(
            self._pipeline_task,
            model=self._model,
            tokenizer=self._tokenizer,
            device_map=self._device_map,
            max_length=self._max_length,
            do_sample=self._do_sample,
            top_k=self._top_k,
            num_return_sequences=self._num_return_sequences,
            eos_token_id=self._tokenizer.eos_token_id
        )