from modelscope import AutoTokenizer, AutoModelForCausalLM, snapshot_download
from convert_to_json import convert_to_json
from get_prompt import get_prompt


model_dir = snapshot_download("qwen/Qwen-14B-Chat-Int4",revision = 'v1.0.5')
# Note: The default behavior now has injection attack prevention off.
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    device_map="auto",
    trust_remote_code=True
).eval()








response, history = model.chat(tokenizer, prompt, history=None)



print(response)

json_response = convert_to_json(response)

print(json_response)

