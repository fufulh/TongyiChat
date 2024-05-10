import json
import random
from http import HTTPStatus
from flask_socketio import SocketIO, emit
from dashscope.api_entities.dashscope_response import Role
from dashscope import Generation

from chat.history import history_conversions
from chat.tools import get_current_time, get_current_weather

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


def get_response(messages):
    response = Generation.call(
        model=Generation.Models.qwen_max,  # 使用指定的模型
        messages=messages,
        result_format='message',  # 设置结果格式为"message"
        tools=tools,
        seed=random.randint(1, 10000),  # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
        stream=True,  # 启用流式传输
        # incremental_output=True  # 增量式流式输出
    )
    return response


def remove_prefix(s, prefix):
    if s.startswith(prefix):
        return s.replace(prefix, '', 1)
    return s


def stream_response(response_stream):
    res = ''
    ans = ''
    # 遍历生成器中的每个响应片段
    for response_chunk in response_stream:
        if response_chunk.status_code == HTTPStatus.OK:
            print(response_chunk)
            for choice in response_chunk.output.choices:
                print(choice['message'])

                # 处理工具调用
                if 'tool_calls' in choice['message'] and choice['finish_reason'] == "tool_calls":
                    process_tool_calls(response_chunk.output.choices[0].message)
                    return
                else:
                    res = remove_prefix(choice['message']['content'], ans)
                    ans = choice['message']['content']
                    # 发送模型的输出到前端
                    emit('response', f"{choice['message']['role']}: {res}")
                    # res = choice['message']['content']
                    # print(choice)
        else:
            emit('error',
                 f'Request id: {response_chunk.request_id}, Status code: {response_chunk.status_code}, error code: {response_chunk.code}, error message: {response_chunk.message}')
    print(ans)
    history_conversions(Role.ASSISTANT, ans)


def process_tool_calls(assistant_output):
    tool_calls = assistant_output.get('tool_calls', [])
    print("tool_calls")
    print(tool_calls)
    for tool_call in tool_calls:
        # 使用字典的键来访问值
        tool_name = tool_call.get('function', {}).get('name')
        if tool_name == "get_current_weather":
            # 将字符串解析为字典
            arguments_str = tool_call.get('function', {}).get('arguments')
            arguments_dict = json.loads(arguments_str) if arguments_str else {}
            location = arguments_dict.get('properties', {}).get('location')
            tool_output = get_current_weather(location)
            print(tool_output)
        elif tool_name == "get_current_time":
            tool_output = get_current_time()
        # 将工具的输出添加到消息列表中，以便模型在下一轮调用中使用
        history_conversions(Role.ASSISTANT, tool_output)
        emit('response', f"{'assistant'}: {tool_output}")
