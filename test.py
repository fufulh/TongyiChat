from http import HTTPStatus
import dashscope
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role

dashscope.api_key = 'sk-0778e34d54d14e88a932ccc17b67c80c'  # 设置您的API_KEY

def conversation_with_messages():
    messages = [{'role': Role.SYSTEM, 'content': 'You are a helpful assistant.'}]

    while True:
        prompt = input("USER: ")
        messages.append({'role': Role.USER, 'content': prompt})

        # 使用流式传输，调用API
        response_stream = Generation.call(
            Generation.Models.qwen_turbo,  # 使用指定的模型
            messages=messages,
            result_format='message',  # 设置结果格式为"message"
            stream=True,  # 启用流式传输
        )

        # 遍历生成器中的每个响应片段
        for response_chunk in response_stream:
            if response_chunk.status_code == HTTPStatus.OK:
                for choice in response_chunk.output.choices:
                    print(f"{choice['message']['role']}: {choice['message']['content']}")
                    # 把模型的输出添加到messages中
                    messages.append({'role': choice['message']['role'],
                                     'content': choice['message']['content']})
            else:
                print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                    response_chunk.request_id, response_chunk.status_code,
                    response_chunk.code, response_chunk.message
                ))
                exit()

if __name__ == '__main__':
    conversation_with_messages()
