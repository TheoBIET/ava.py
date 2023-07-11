from utils.constants import *
from classes.openai_requester import OpenAI

class ChatBot:
    def __init__(self):
        self._use_local = CHATBOT_USE_LOCAL
        self._max_length = CHATBOT_MAX_LENGTH
        
        if self._use_local:
            self._local_model = CHATBOT_LOCAL_MODEL
            self._pipeline_task = CHATBOT_LOCAL_PIPELINE_TASK
            self._cache_dir = CHATBOT_LOCAL_CACHE_DIR
            self._initializeLocal()
            print(f'🤖 Using Local ChatBot')
        else:
            self._openai = OpenAI()
            print(f'🤖 Using OpenAI ChatBot')
    
    # TODO: Test local model
    def chat(self, input):
        if self._use_local: return self._getSequence(input)
        else: return self._openai.chat(input, max_tokens=self._max_length)
    
    # TODO: Test local model
    def _getSequence(self, input):
        sequences = pipeline(
            input,
            max_length=200,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
        )
        
        return sequences[0]['generated_text']
    
    # TODO: Test local model
    def _initializeLocal(self):
        self._tokenizer = AutoTokenizer.from_pretrained(
            self._local_model,
            cache_dir=FALCON_CACHE_DIR
        )

        self._model = AutoModelForCausalLM.from_pretrained(
            self._local_model,
            cache_dir=FALCON_CACHE_DIR, 
            torch_dtype=torch.bfloat16,
            trust_remote_code=FALCON_TRUST_REMOTE_CODE,
            device_map=FALCON_DEVICE_MAP,
            offload_folder=FALCON_OFFLOAD_FOLDER
        )

        self._pipeline = transformers.pipeline(
            FALCON_PIPELINE_TASK,
            model=model,
            tokenizer=tokenizer,
            device_map=FALCON_DEVICE_MAP,
            max_length=FALCON_PIPELINE_MAX_LENGTH,
            do_sample=FALCON_PIPELINE_DO_SAMPLE,
            top_k=FALCON_PIPELINE_TOP_K,
            num_return_sequences=FALCON_PIPELINE_NUM_RETURN_SEQUENCES,
            eos_token_id=tokenizer.eos_token_id
        )