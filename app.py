import os
import traceback
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from script.deal_excel import process_outputFilepath, process_excelFilepath, getOutdir, pre_deal, get_col, \
    create_union_excel

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


@app.route('/getfilepath', methods=['POST'])
def process_data():
    data = request.get_json()
    outputFilepath = data['outputFilepath']
    process_outputFilepath(outputFilepath)
    print("outputFilepath", outputFilepath)
    return 'getfilepath successfully'


@app.route('/upload', methods=['POST'])
@app.route('/getfile', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    filepath = os.path.dirname(__file__)
    save_path = os.path.join(os.path.dirname(__file__), 'temp', filename)
    file.save(save_path)
    process_excelFilepath(filename, save_path)
    print("filepath", filepath)
    print("savepath", save_path)
    return 'File uploaded successfully'


if __name__ == '__main__':
    app.run()
