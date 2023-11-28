#!/usr/bin/python3

from aiohttp import web
import asyncio
import qwen_cpp

import copy
import os
import platform
import time
import readline
import json
from shutil import copyfile

pipeline = qwen_cpp.Pipeline('./qwen.cpp/qwen14b-ggml.bin', './qwen.cpp/qwen.tiktoken')


# history = ["Bunny说: 今天吃什么好呢？"]
# T1 = time.time()
# response = pipeline.chat(history, top_p=0.8, temperature=1)
# T2 = time.time()
# print('程序运行时间:%s毫秒' % ((T2 - T1) * 1000))
# print(type(response))
# print(response)

address = '0.0.0.0'
port = '48283'

async def handle(request):
    data = await request.json()
    history = data['history']
    print(type(history))

    query = data['query']
    if history == None:
        history = [query]
    else:
        history.append(query)
    print(query)
    T1 = time.time()
    response = pipeline.chat(history, top_p=0.8, temperature=1)
    T2 = time.time()
    print('程序运行时间:%s毫秒' % ((T2 - T1) * 1000))
    print(response)
    return web.Response(text=response)

app = web.Application()
app.add_routes([web.post('/', handle)])
web.run_app(app, host=address, port=port)