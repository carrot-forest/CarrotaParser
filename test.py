from modelscope import AutoTokenizer, AutoModelForCausalLM, snapshot_download



model_dir = snapshot_download("qwen/Qwen-14B-Chat-Int4",revision = 'v1.0.5')
# Note: The default behavior now has injection attack prevention off.
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    device_map="auto",
    trust_remote_code=True
).eval()

question = "查询数学作业"

#prompt = "现在，你是一个专业的语句解析助手。你的面前有如下若干接口可以调用。我将告诉你一句话，这句话期望调用这些接口中的任意多个。请你解析这句话，判断需要调用哪些接口；如果调用，需要传入哪些参数。\n\n1.复读机: 传入一个参数复读的内容，将返回一个复读的内容。是一定都要被调用的插件，无论你认为需不需要调用。\n\n解析完成后，你需要以如下格式输出你的解析结果，请给出所有插件的是否需要的回答：\n\n1.[调用/不调用]\n\n例如，如果解析语句“今天天气怎么样”，你应当输出：\n\n1.调用\n\n现在，你需要解析的语句是：" + question


prompt_path = './prompt_test.txt'
prompt = open(prompt_path).read() + question

#prompt = get_prompt(json_list, question)
print(prompt)
#prompt1 = "现在，你是一个专业的语句解析助手。你的面前有如下若干接口可以调用。我将告诉你一句话，这句话期望调用这些接口中的任意多个。请你解析这句话，判断需要调用哪些接口；如果调用，需要传入哪些参数。\n\n1. 天气查询: 传入一个参数即地点，将返回这个地点的天气。如果你认为需要进行天气查询，但语句中没有给出地点，请传入“武汉”。\n\n解析完成后，你需要以如下格式输出你的解析结果，请给出所有插件的是否需要的回答：\n\n1. [调用/不调用] [地点]\n\n例如，如果解析语句“今天天气怎么样”，你应当输出：\n\n1. 调用 武汉\n\n现在，你需要解析的语句是：\今天温度多少"
response, history = model.chat(tokenizer, prompt, history=None)

#print(type(history))

print(response)

#json_response = convert_to_json(response)

#print(json_response)
# 你好！很高兴为你提供帮助。
