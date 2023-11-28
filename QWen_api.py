from modelscope import AutoTokenizer, AutoModelForCausalLM, snapshot_download

import copy
import os
import platform
import time
import readline
import json
from shutil import copyfile
from aiohttp import web


model_dir = snapshot_download("qwen/Qwen-14B-Chat-Int4",revision = 'v1.0.5')
# Note: The default behavior now has injection attack prevention off.
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)



model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    device_map="auto",
    trust_remote_code=True
).eval()
# query = "今天天气好像很好呢"
# history = None
# prompt_path = 'prompt_wrap.txt'
# prompt = open(prompt_path).read() + "\n" + query
# T1 = time.time()
# response, history = model.chat(tokenizer, prompt, history=history)
# T2 = time.time()
# print('程序运行时间:%s毫秒' % ((T2 - T1) * 1000))
# print(response)
address = '0.0.0.0'
port = '48283'

async def handle(request):
    print("\n\n\n\n\n\n\n")
    data = await request.json()
    #print(data)
    prompt_path = data['prompt']
    print("\n\n\n\n\n\n\n this is prompt_path:{}\n\n\n\n\n\n".format(prompt_path) )
    prompt = open(prompt_path).read()
    print(prompt)
    query = data['query']
    print(query)
    print(type(query))
    if (query == None) or (query == ""):
        response, history = model.chat(tokenizer, prompt, history=None)
    else:
        response, history = model.chat(tokenizer, prompt, history=None)
        print(history)
        print("\n\n\n\n\n\n")
        history_list = data['history']
        if history_list != None:
            history = history + [history_list[i:i+2] for i in range(0,len(history_list),2)]
        print(history)
        print("\n\n\n\n\n\n")
        response, history = model.chat(tokenizer, query, history=history)
    #print('用户提问:\n  ',query)
    #print('历史消息:\n  ',history)
        
    

    
    
    T1 = time.time()

    print("this is response:")
    print(type(response))
    print(response)
        
    #print("\n\n\n\n多少沾点逆天")
    T2 = time.time()
    print('\n\n\n\n程序运行时间:%s毫秒' % ((T2 - T1) * 1000))
    
    return web.Response(text=response)

app = web.Application()
app.add_routes([web.post('/', handle)])
web.run_app(app, host=address, port=port)