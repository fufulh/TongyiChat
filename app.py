import dashscope

from flask import Flask, request, jsonify,render_template

from chat.history import history_conversions, messages
from chat.streamchat import get_response, stream_response
from image_generator import generate_images
from flask_socketio import SocketIO, emit
from dashscope.api_entities.dashscope_response import Role
from http import HTTPStatus
dashscope.api_key = "sk-0778e34d54d14e88a932ccc17b67c80c"

from database.base import engine, Base

def create_tables():
    Base.metadata.create_all(engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app, cors_allowed_origins='*')
name_space = '/dashscope'



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/image')
def iamge():
    return render_template('image.html')


@socketio.on('connect', namespace=name_space)
def handle_connect():
    print('Client connected')


@socketio.on('disconnect', namespace=name_space)
def handle_disconnect():
    print('Client disconnected')


@socketio.on('message', namespace=name_space)
def handle_message(message):
    print('Received message: ' + message)
    history_conversions(Role.USER, message)
    print(messages)
    response_stream = get_response(messages)
    # 使用流式传输，调用API
    stream_response(response_stream)


@app.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.get_json()
    print(data)
    prompt = data.get('prompt', 'Mouse rides elephant')
    file_paths, error = generate_images(prompt)
    if file_paths:
        # 返回图像文件的路径给前端
        return jsonify({'image_url': file_paths})
    else:
        # 返回错误信息
        return jsonify({'error': error}), HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    create_tables()
