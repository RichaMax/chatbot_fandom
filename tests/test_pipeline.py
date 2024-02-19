from chatbot.pipeline.qa_pipeline import QAPipeline, QAPipelineAPI
from langchain.chains import RetrievalQA
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
# my_pipeline = QAPipelineAPI()

# print(my_pipeline("What is the size of the Earth?"))

# my_pipeline = QAPipeline()

# # print(my_pipeline("Instruct: Answer only to the question What is the size of the Earth?\nOutput:", max_length=100))
# print(my_pipeline("Answer to the question as succinctly as possible, What is the diameter of the Earth?",
#                   max_new_tokens=100)
#       )

from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)

# messages = [
#     {"role": "user", "content": "What is your favourite condiment?"},
#     {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
#     {"role": "user", "content": "Do you have mayonnaise recipes?"}
# ]

# encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")
# Define the conversation prompt
conversation_prompt = "Answer to the question as succinctly as possible, What is the diameter of the Earth?"

# Generate a response
input_ids = tokenizer.encode(conversation_prompt, return_tensors="pt")
bot_response = model.generate(input_ids, max_length=200, temperature=0.9, do_sample=True)

# Decode and print the response
response_text = tokenizer.decode(bot_response[0])
print(response_text)