
from zipfile import ZipFile
from flask import Flask, request, render_template
import os, espBuilder, shutil

var = "test"
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if not os.path.isdir('./product'):
        os.mkdir('product')
    else:
        shutil.rmtree('product')
    if not os.path.isdir('./upload'):
        os.mkdir('upload')
    else:
        shutil.rmtree('upload')

    file = request.files['file']
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



    return render_template('index.html', uploadSuccess=True)

