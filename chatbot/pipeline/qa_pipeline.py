import os

from huggingface_hub import InferenceClient
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


class QAPipelineAPI:
    def __init__(self, config: dict | None = None):
        if config is None:
            config = {}
        model_name = "microsoft/phi-2"
        # tokenizer = AutoTokenizer.from_pretrained(model_id)

        # model_kwargs = config.get("model_args", {})
        # model = AutoModelForCausalLM.from_pretrained(model_id, **model_kwargs)
        self.client = InferenceClient(model=model_name, token=os.environ["HF_TOKEN"])

    def __call__(self, text, **kwargs):
        response = self.client.post(json={"inputs":text})
        return response.json()


class QAPipeline:
    def __init__(self, config: dict | None = None):
        if config is None:
            config = {}
        model_id = "microsoft/phi-2"
        tokenizer = AutoTokenizer.from_pretrained(model_id, torch_dtype="auto", trust_remote_code=True, skip_special_tokens=False)

        model_kwargs = config.get("model_args", {})
        model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
        self.pipeline = pipeline(task="text-generation", model=model, tokenizer=tokenizer, device="cpu", return_full_text = False)

    def __call__(self, text, **kwargs):
        return self.pipeline(text, **kwargs)
