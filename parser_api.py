import copy
import os
import platform
import time
import readline
import json
from shutil import copyfile
from aiohttp import web
import requests
from propose_prompt_response import get_prompt
from propose_prompt_response import convert_to_json


address = '0.0.0.0'
port = '5001'

def convert_prompt(prompt):
    total_data = {}
    total_data['history'] = None
    total_data['prompt'] = prompt
    total_data['query'] = None
    total_data = json.dumps(total_data)
    return total_data

async def handle(request):
    
    print("this is request:{}".format(request))
    
    data = await request.json()
    
    print("this is data:{}".format(data))
    
    message = data['message']
    
    print("this is message:{}".format(message))
    
    url_list = " http://192.168.192.5:3435/api/v1/plugin/list"
    jsonList = requests.get(url_list)
    
    print("this is response_status_code: {}".format(jsonList.status_code) )
    print("this is response text:{}".format(jsonList.text))
    
    
    json_data = json.loads(jsonList.text)
    json_list = json_data['data']
    
    print("this is json_list:{}".format(json_list))
    
    prompt = get_prompt(json_list, message)
    
    
    print("\n\n\n\n\===============================================\n\n\n\n")
    print("this is prompt:{}".format(prompt))
    print("\n\n\n\n\===============================================\n\n\n\n")
    with open(f'prompt_parser.txt','w') as f:
        f.writelines(prompt)
    
    prompt_path = './prompt_parser.txt'
        
    # post QWen
    T1 = time.time()
    #response, history = model.chat(tokenizer, prompt, history=history)
    
    url_QWen = 'http://127.0.0.1:48283'
    
    total_data = convert_prompt(prompt_path)
    
    print("\n\n\n\n\nthis is total_data:{}\n\n\n\n\n".format(total_data))
    
    parsed_response = requests.post(url_QWen, data = total_data)
    
    T2 = time.time()
    
    print("this is parse response:{}".format(parsed_response.text))
    
    parsed_response = parsed_response.content.decode()
    
    print("\n\n\n\n\n{}\n\n\n\n\n".format(parsed_response))
    
    response = convert_to_json(parsed_response, json_list)
    
    print("this is response:{}".format(response))
    
    print('程序运行时间:%s毫秒' % ((T2 - T1) * 1000))
    
    
    
    return web.Response(text=response)

app = web.Application()
app.add_routes([web.post('/parser', handle)])
web.run_app(app, host=address, port=port)