import os
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
    return render_template('test.html')

# 上传合并文件父路径
@app.route('/set_union_outdir', methods=['POST'])
def set_path():
    path = request.json['path']
    set_union_outdir(path)
    return jsonify({'path': path})

# 上传文件，将其保存在合并文件父路径中
@app.route('/upload', methods=['POST'])
@app.route('/getfile', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    union_outdir = get_union_outdir()
    save_path = os.path.join(union_outdir, filename)
    print("save_path", save_path)
    file.save(save_path)
    return 'File uploaded successfully'


@app.route('/merge', methods=['POST'])
def merge():
    print("请求进入deal_excel")
    deal_excel.main()
    return "deal_excel.py成功执行"


if __name__ == '__main__':
    app.run()
