
from zipfile import ZipFile
from flask import Flask, request, redirect, url_for, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    zipped_file = file.stream._file
    with ZipFile(zipped_file, 'r') as zip_ref:
        zip_ref.extractall('upload')


    return "<p>File Successfully uploaded!</p>"

