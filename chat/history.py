

messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]


def history_conversions(role, message):
    messages.append({'role': role, 'content': message})
