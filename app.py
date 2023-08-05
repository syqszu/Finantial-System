import os
import subprocess
import traceback
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from script.deal_excel import process_union_outdir

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
union_outdir = ""

@app.errorhandler(Exception)
def handle_exception(e):
    print(traceback.format_exc())
    return 'Internal Server Error', 500


@app.route('/')
def index():
    # return render_template('indexshan.html')
    return render_template('test.html')

# 上传合并文件父路径
@app.route('/set_union_outdir', methods=['POST'])
def set_path():
    path = request.json['path']
    union_outdir = path
    process_union_outdir(path)
    return jsonify({'path': path})

file_names = []
@app.route('/upload', methods=['POST'])
@app.route('/getfile', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file_names.append(filename)
    save_path = os.path.join(union_outdir, filename)
    file.save(save_path)

    return 'File uploaded successfully'

@app.route('/get_file_info', methods=['GET'])
def get_file_info():
    return jsonify({'file_names': file_names})

if __name__ == '__main__':
    app.run()
