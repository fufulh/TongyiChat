import dashscope
from dashscope import Generation
from datetime import datetime
import random
import json
dashscope.api_key = 'sk-0778e34d54d14e88a932ccc17b67c80c'  # 设置您的API_KEY
# 定义工具列表，模型在选择使用哪个工具时会参考工具的name和description
tools = [
    # 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}  # 因为获取当前时间无需输入参数，因此parameters为空字典
        }
    },
    # 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {  # 查询天气时需要提供位置，因此参数设置为location
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                }
            },
            "required": [
                "location"
            ]
        }
    }
]


# 模拟天气查询工具。返回结果示例：“北京今天是晴天。”
def get_current_weather(location):
    return f"{location}今天是晴天。 "


# 查询当前时间的工具。返回结果示例：“当前时间：2024-04-15 17:15:18。“
def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"


# 封装模型响应函数
def get_response(messages):
    response = Generation.call(
        model='qwen-max',
        messages=messages,
        tools=tools,
        seed=random.randint(1, 10000),  # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
        result_format='message',  # 将输出设置为message形式
        stream=True,
        # incremental_output=True  # 增量式流式输出
    )
    return response


def call_with_messages():
    print('\n')
    messages = [
        {
            "content": input('请输入：'),  # 提问示例："现在几点了？" "一个小时后几点" "北京天气如何？"
            "role": "user"
        }
    ]

    # 模型的第一轮调用
    first_response = get_response(messages)
    for first__chunk in first_response:
        assistant_output = first__chunk.output.choices[0].message
        print(f"\n大模型第一轮输出信息：{first__chunk}\n")
        # messages.append(assistant_output)
        # if 'tool_calls' not in assistant_output:  # 如果模型判断无需调用工具，则将assistant的回复直接打印出来，无需进行模型的第二轮调用
        #     print(f"最终答案：{assistant_output.content}")
        #     return
        # # 如果模型选择的工具是get_current_weather
        # elif assistant_output.tool_calls[0]['function']['name'] == 'get_current_weather':
        #     tool_info = {"name": "get_current_weather", "role": "tool"}
        #     location = json.loads(assistant_output.tool_calls[0]['function']['arguments'])['properties']['location']
        #     tool_info['content'] = get_current_weather(location)
        # # 如果模型选择的工具是get_current_time
        # elif assistant_output.tool_calls[0]['function']['name'] == 'get_current_time':
        #     tool_info = {"name": "get_current_time", "role": "tool"}
        #     tool_info['content'] = get_current_time()
        # print(f"工具输出信息：{tool_info['content']}\n")
        # messages.append(tool_info)
        #
        # # 模型的第二轮调用，对工具的输出进行总结
        # second_response = get_response(messages)
        # print(f"大模型第二轮输出信息：{second_response}\n")
        # print(f"最终答案：{second_response.output.choices[0].message['content']}")


if __name__ == '__main__':
    call_with_messages()
