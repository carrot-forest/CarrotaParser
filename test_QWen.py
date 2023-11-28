from modelscope import AutoModelForCausalLM, AutoTokenizer
from modelscope import GenerationConfig
from modelscope import AutoTokenizer, AutoModelForCausalLM, snapshot_download

# 可选的模型包括: "qwen/Qwen-7B-Chat", "qwen/Qwen-14B-Chat"

model_dir = snapshot_download("qwen/Qwen-14B-Chat-Int4",revision = 'v1.0.5')
# Note: The default behavior now has injection attack prevention off.
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)



model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    device_map="auto",
    trust_remote_code=True
).eval()


response, history = model.chat(tokenizer, "你好", history=None)
print(response)
response, history = model.chat(tokenizer, "浙江的省会在哪里？", history=history) 
print(response)
response, history = model.chat(tokenizer, "它有什么好玩的景点", history=history)
print(response)

print(history)
