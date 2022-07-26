from flask import Flask, request, redirect, url_for, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    # return "<p>test</p>"

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return "<p>File Successfully uploaded!</p>"

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['the_file']
#         f.save('/var/www/uploads/uploaded_file.txt')
#         return "<p>Hello, World!</p>"