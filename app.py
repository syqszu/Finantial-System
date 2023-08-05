import os
import subprocess
import traceback
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

from script.deal_excel_shan import process_outputFilepath, process_excelFilepath, getOutdir, pre_deal, get_col, \
    create_union_excel, judgeprocess

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.errorhandler(Exception)
def handle_exception(e):
    print(traceback.format_exc())
    return 'Internal Server Error', 500


@app.route('/')
def index():
    # return render_template('indexshan.html')
    return render_template('test.html')



@app.route('/set_output_path', methods=['POST'])
def set_path():
    path = request.json['path']
    # 处理路径，例如保存到数据库或进行其他操作
    # ...
    return jsonify({'path': path})

@app.route('/getfilepath', methods=['POST'])
def process_data():
    data = request.get_json()
    outputFilepath = data['outputFilepath']
    process_outputFilepath(outputFilepath)
    print("outputFilepath", outputFilepath)
    return 'getfilepath successfully'

# 全局变量，用以记录已收到的文件数量
filecnt = 0
file_names = []
@app.route('/upload', methods=['POST'])
@app.route('/getfile', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file_names.append(file.filename)
    filepath = os.path.dirname(__file__)
    save_path = os.path.join(os.path.dirname(__file__), 'temp', filename)
    file.save(save_path)
    global filecnt
    filecnt += 1
    process_excelFilepath(filename, save_path)
    print("filepath", filepath)
    print("savepath", save_path)
    return 'File uploaded successfully'


@app.route('/get_file_info', methods=['GET'])
def get_file_info():
    return jsonify({'file_names': file_names})

if __name__ == '__main__':
    app.run()
