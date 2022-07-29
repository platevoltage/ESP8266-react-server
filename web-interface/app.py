
from zipfile import ZipFile
from flask import Flask, request, render_template, send_from_directory
import os, espBuilder, shutil

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
    
    
    espBuilder.createRootDirectory()
    espBuilder.createDirs(".")
    espBuilder.createAssetArray()
    espBuilder.createFileDirectoryChunk()
    espBuilder.createWifiChunk()
    espBuilder.createRestPathChunk()
    espBuilder.createIno()

    directoryTree = listDirectoryTree('./product/react-server/')
    
    shutil.make_archive('./product/react-server', 'zip', './product/react-server')
    return render_template('index.html', uploadSuccess=True, directoryTree=directoryTree)

@app.route('/download/')
def download():

    return send_from_directory(directory="./product", path="./react-server.zip")


def listDirectoryTree(directory):
    tree = []
    text = ''
    
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = '-' * 4 * (level)
        # indent = ''
        tree.append('{}{}/'.format(indent, os.path.basename(root)))
        subindent = '-' * 4 * (level + 1)
        # subindent = ''
        for f in files:
            tree.append('{}{}'.format(subindent, f))
    for line in tree:
        print(line)
        text += line + '\n'
    print(tree)
    return tree