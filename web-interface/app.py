
from zipfile import ZipFile
from flask import Flask, request, render_template, send_from_directory
import os, espBuilder, shutil

var = "test"
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    espBuilder.ssid = request.form['ssid']
    espBuilder.password = request.form['password']
    
    if os.path.isdir('./product'):
        shutil.rmtree('product')
    if os.path.isdir('./upload'):
        shutil.rmtree('upload')
    os.mkdir('product')   
    os.mkdir('upload')

    
    zipped_file = file.stream._file
    with ZipFile(zipped_file, 'r') as zip_ref:       
        zip_ref.extractall('upload')
    
    workingDirectory = os.listdir('./upload')[-1]
    print(os.listdir('./upload/' + workingDirectory))
    
    espBuilder.createRootDirectory()
    espBuilder.createDirs(".")
    espBuilder.createAssetArray()
    espBuilder.createFileDirectoryChunk()
    espBuilder.createWifiChunk()
    espBuilder.createRestPathChunk()
    espBuilder.createIno()


    shutil.make_archive('./product/react-server', 'zip', './product/react-server')
    return render_template('index.html', uploadSuccess=True)

@app.route('/download/')
def download():

    return send_from_directory(directory="./product", path="./react-server.zip")