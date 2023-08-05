import os
import subprocess
import traceback
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import deal_excel
from script.modify import set_union_outdir, get_union_outdir

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

# 上传合并文件父路径
@app.route('/set_union_outdir', methods=['POST'])
def set_path():
    path = request.json['path']
    set_union_outdir(path)
    return jsonify({'path': path})


@app.route('/upload', methods=['POST'])
@app.route('/getfile', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    union_outdir = get_union_outdir()
    save_path = os.path.join(union_outdir, filename)
    print("save_path",save_path)
    file.save(save_path)
    return 'File uploaded successfully'

@app.route('/run_deal_excel')
def run_main():
    # result = subprocess.run(['python', 'deal_excel.py'], capture_output=True, text=True, check=True)
    # print("result.stdout")
    # print(result.stdout)
    # if result.returncode == 0:
    #     return 'deal_excel.py 已成功执行'
    # else:
    #     return 'deal_excel.py 执行失败'
    deal_excel.main()
    return "deal_excel.py成功执行"

if __name__ == '__main__':
    app.run()
