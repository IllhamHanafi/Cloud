from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, jsonify, send_file
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from Auth_Model import *
from Users_Model import *
import os

from flask_autoindex import AutoIndex 


app = Flask(__name__)
users_list = Users_Model()
# UPLOAD_FOLDER = '/home/bujang/dummy' #ganti ini pake directory kalian
# USER_UPLOAD_FOLDER = '/home/bujang/dummy' #ganti ini pake directory kalian
UPLOAD_FOLDER = os.path.dirname(os.getcwd()) #ganti ini pake directory kalian
USER_UPLOAD_FOLDER = os.path.dirname(os.getcwd()) #ganti ini pake directory kalian
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3'])
app.config['USER_UPLOAD_FOLDER'] = USER_UPLOAD_FOLDER

index = AutoIndex(app, USER_UPLOAD_FOLDER, add_url_rules=False)

a_model = Auth_Model()
activeToken = ''
Bootstrap(app)

def authenticate():
    flag_authorized = a_model.cek_token(activeToken)
    if (flag_authorized is None):
        return False
    else:
        return True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def make_tree(path):
    tree = dict(name=path, children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=fn))
    return tree

def list_diretory(path):
    files = os.listdir(path)
    return files

@app.route("/")
def home():
    if not authenticate():
        return redirect('/login')
    else:
        # return render_template('home.html', filelist=make_tree(USER_UPLOAD_FOLDER))
        return render_template('home.html', filelist=list_diretory(USER_UPLOAD_FOLDER))

@app.route('/login', methods=['GET', 'POST'])
def login():
    global USER_UPLOAD_FOLDER
    global activeToken
    if request.method == 'POST':
        if users_list.login(request.form['username'], request.form['password']):
            USER_UPLOAD_FOLDER = UPLOAD_FOLDER + '/' + request.form['username']
            app.config['USER_UPLOAD_FOLDER'] = USER_UPLOAD_FOLDER
            activeToken = a_model.get_token(request.form['username'], users=users_list)
            return redirect('/')
        else:
            flash('Wrong Username / Password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    global USER_UPLOAD_FOLDER
    if request.method == 'POST':
        if users_list.add(request.form['username'], request.form['password']):
            flash('Create Account Success !')
#            session['logged_in'] = True
            USER_UPLOAD_FOLDER = UPLOAD_FOLDER + '/' + request.form['username']
            if not os.path.exists(USER_UPLOAD_FOLDER):
                os.makedirs(USER_UPLOAD_FOLDER)
            app.config['USER_UPLOAD_FOLDER'] = USER_UPLOAD_FOLDER
            return redirect('/')
        else:
            flash('Username Already Exist !')
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    global activeToken
    activeToken = ''
    return redirect('/')

@app.route("/upload")
def upload():
    if not authenticate():
        return redirect('/login')
    else:
        return render_template('upload.html')

@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = filename.replace("_", " ")
            file.save(os.path.join(app.config['USER_UPLOAD_FOLDER'], filename))
#            return redirect(url_for('uploaded_file',
#                                    filename=filename))
            return 'file uploaded successfully'
    else:
        return 'failed to upload file'

@app.route('/download/<file>')
def download(file):
    path_to_download = USER_UPLOAD_FOLDER+'/'+file
    return send_file(path_to_download, attachment_filename=file, as_attachment=True)


@app.route('/index')
def autoindex():
    if not authenticate():
        return redirect('/login')
    else:
        hasil = list_diretory(USER_UPLOAD_FOLDER)
        hasil = jsonify(hasil)
        return hasil

@app.route('/tree')
def cobatree():
    rambo = USER_UPLOAD_FOLDER
    hasil = make_tree(rambo)
    hasil = jsonify(hasil)
    return hasil

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #max upload 16 mb
    app.run(debug=True)
