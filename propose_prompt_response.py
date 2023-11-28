import json

def get_prompt(json_list, query):
    head = "现在，你是一个专业的语句解析助手。你的面前有如下若干接口可以调用。我将告诉你一句话，这句话期望调用这些接口中的任意多个。请你解析这句话，判断需要调用哪些接口；如果调用，需要传入哪些参数。\n\n"
    plug_content = []
    answer_prompt_head = "\n\n解析完成后，你需要以如下格式输出你的解析结果，请给出所有插件的是否需要的回答：\n\n"
    answer_prompt = []
    example_prompt_head = "\n\n例如，如果解析语句“今天天气怎么样”，你应当输出：\n\n"
    example_prompt = []
    query_prompt_head = "\n\n现在，你需要解析的语句是：\n"
    query_prompt = query
    
    for i, json_obj in enumerate(json_list, start=1):
        #json_obj = json.load(json_str)
        
        name = json_obj.get("name","")
        description = json_obj.get("description", "")
        
        answer_head = "[调用/不调用]"
        param_key = None
        param_key_str = None
        
        if(json_obj.get("param", []) != None):
            param_key = [param["key"] for param in json_obj.get("param", [])]
            param_key_str = " ".join([ "[" + key + "]" for key in param_key])
            answer_prompt.append(f"{i}.{answer_head} {param_key_str} \n")
        else:
            answer_prompt.append(f"{i}.{answer_head} \n")
        
        #print("\n\n\n\nthis is answer_prompt:{} \n\n\n\n\n".format(answer_prompt))
        
        
        
        examples = json_obj.get("example", "")
        
        print("\n\n\n\n\n this is examples:{}".format(examples))
        examples = examples[0]
        
        
        #param_key_str = " ".join([ "[" + key + "]" for key in param_key])
        #example_str = " ".join(examples)
        
        
        
        plug_content.append(f"{i}.{name}: {description}\n")
        
        example_prompt.append(f"{i}.{examples}\n")
    
    
    prompt = head + "".join(plug_content) + answer_prompt_head + "".join(answer_prompt) + example_prompt_head + "".join(example_prompt) + query_prompt_head + query_prompt
    return prompt
    
def convert_to_json(response, json_list):
    
    response_lines = response.strip().split('\n')
    print("\n\n\n this is  hahhahahahah:{}".format(response_lines))
    response_dict = {}
    plugin_list = []
    
    for line in response_lines:
        
        
        
        parts = line.split('.')
        key = parts[0]
        value = parts[1].split()
        
        print("\n\n\nthis is line hahahhahahah :{}\n\n\n".format(line))
        
        if(value[0] == "不调用"):
            print("======================\n\n\n\n\n\n")
            print("这个插件不被调用")
            print("======================\n\n\n\n\n\n")
            print("this is value: {}".format(value))
            print("======================\n\n\n\n\n\n")
            print("======================\n\n\n\n\n\n")
            continue
        
        print("现在开始解析参数")
        
        plugin_now = json_list[int(key) - 1]
        
        plugin_id = plugin_now.get("id","")
        
        plugin_json = {}
        plugin_json["id"] = plugin_id
        
        if(value[0] == "调用" and plugin_now.get("param", []) != None):
            print("======================\n\n\n\n\n\n")
            print("this is value: {}".format(value))
            print("======================\n\n\n\n\n\n")
            value_dictory = {}
            params = [param["key"] for param in plugin_now.get("param", [])]
            
            print("======================\n\n\n\n\n\n")
            print("这是我的params: {}".format(params))
            print("======================\n\n\n\n\n\n")
            
            for i in range(1, min(len(params), len(value)) ):
                value_dictory[params[i - 1]] = value[i]
            
            plugin_json["param"] = value_dictory
           
        else:
             plugin_json["param"] = None
            
       
        
        plugin_list.append(plugin_json)
    
    response_dict["plugin"] = plugin_list
    json_response = json.dumps(response_dict, indent=4, ensure_ascii = False)
    
    return json_response


#response = "1.调用 武汉"

'''
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
'''



#print(convert_to_json(response, json_list))
