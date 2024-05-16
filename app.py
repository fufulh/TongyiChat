import dashscope
from datetime import datetime
from flask import Flask, request, jsonify,render_template

from chat.history import history_conversions, messages
from chat.streamchat import get_response, stream_response
from image_generator import generate_images
from flask_socketio import SocketIO, emit
from dashscope.api_entities.dashscope_response import Role
from model.check_login import is_existed,exist_user,is_null,update_login_time
from model.regist_login import add_user
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


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':  # 注册发送的请求为POST请求
        current_time = datetime.now()
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password, id):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('login.html', message=login_massage)
        elif is_existed(username, password):
            update_login_time(username, password)
            return render_template('index.html', username=username)
        elif exist_user(username):
            login_massage = "温馨提示：密码错误，请输入正确密码"
            return render_template('login.html', message=login_massage)
        else:
            login_massage = "温馨提示：不存在该用户，请先注册"
            return render_template('login.html', message=login_massage)
    return render_template('login.html')


@app.route("/regiser", methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        current_time = datetime.now()
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password, id):
            login_massage = "温馨提示：ID、账号和密码是必填"
            return render_template('register.html', message=login_massage)
        elif exist_user(username):
            login_massage = "温馨提示：用户已存在，请直接登录"
            # return redirect(url_for('user_login'))
            return render_template('register.html', message=login_massage)
        else:
            add_user(request.form['id'], request.form['username'], request.form['password'], current_time_str)
            return render_template('login.html', username=username)
    return render_template('register.html')



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    create_tables()
