from http import HTTPStatus
from flask import Flask, request, jsonify
from image_generator import generate_images

def create_app():
    app = Flask(__name__)

    @app.route('/generate_image', methods=['POST'])
    def generate_image():
        data = request.get_json()
        prompt = data.get('prompt', 'Mouse rides elephant')
        file_path, error = generate_images(prompt)
        if file_path:
            # 返回图像文件的路径给前端
            return jsonify({'image_url': file_path})
        else:
            # 返回错误信息
            return jsonify({'error': error}), HTTPStatus.INTERNAL_SERVER_ERROR

    return app
