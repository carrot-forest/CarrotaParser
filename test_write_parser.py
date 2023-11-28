from propose_prompt_response import get_prompt


json_list = [
    {
    "id": "climate_query",
    "name": "天气查询",
    "description": "传入一个参数即地点，将返回这个地点的天气。如果你认为需要进行天气查询，但语句中没有给出地点，请传入“武汉”。",
    "param": [
      {
        "key": "地点",
        "type": "string",
        "description": "需要查询温度的地区"
      }
    ],
    "examples": 
     "调用 武汉"
    ,
    "url": "https://homework.carrot.cool/api/v1/message"
  }
]

message = '组原报告什么时候截止'




prompt = get_prompt(json_list, message)

with open(f'prompt_parser.txt','w') as f:
    f.writelines(prompt)