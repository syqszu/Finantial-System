import os

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


import traceback

@app.errorhandler(Exception)
def handle_exception(e):
    print(traceback.format_exc())
    return 'Internal Server Error', 500


@app.route('/')
def index():
    return render_template('indexshan.html')
    # return render_template('test.html')


@app.route('/getfilepath', methods=['POST'])
def process_data():
    data = request.get_json()
    jinxiangFilepath = data['jinxiangFilepath']
    xiaoxiangFilepath = data['xiaoxiangFilepath']
    outputFilepath = data['outputFilepath']

    print("jinxiangFilepath", jinxiangFilepath)
    print("xiaoxiangFilepath", xiaoxiangFilepath)
    return jsonify({'result': '处理成功'})


# @app.route('/upload', methods=['POST'])
# def upload():
#     files = request.files.getlist('files')
#     # 处理上传的文件
#     for file in files:
#         filename = file.filename
#         file.save(filename)
#         print("filename", filename)
#         # 在这里可以对文件进行进一步处理
#
#     return 'Upload successful'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    save_path = os.path.join(os.path.dirname(__file__), 'temp', filename)
    file.save(save_path)
    return 'File uploaded successfully'


if __name__ == '__main__':
    app.run()
