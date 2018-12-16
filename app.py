from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from werkzeug.utils import secure_filename
from Users_Model import *
import os

app = Flask(__name__)
users_list = Users_Model()
UPLOAD_FOLDER = '/home/bujang/dummy' #ganti ini pake directory kalian
USER_UPLOAD_FOLDER = '/home/bujang/dummy'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3'])
app.config['USER_UPLOAD_FOLDER'] = USER_UPLOAD_FOLDER

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

@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global USER_UPLOAD_FOLDER
#    if request.form['username'] == 'admin' and request.form['password'] == 'admin':
#        session['logged_in'] = True
    if users_list.find(request.form['username'], request.form['password']):
        session['logged_in'] = True
        USER_UPLOAD_FOLDER = UPLOAD_FOLDER + '/' + request.form['username']
        app.config['USER_UPLOAD_FOLDER'] = USER_UPLOAD_FOLDER
    else:
        flash('Wrong Username / Password')
    return home()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if users_list.add(request.form['username'], request.form['password']):
            flash('Create Account Success !')
            session['logged_in'] = True
            return render_template('home.html')
        else:
            flash('Username Already Exist !')
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return home()

@app.route("/upload")
def upload():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('upload.html', filelist=make_tree(USER_UPLOAD_FOLDER))

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

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #max upload 16 mb
    app.run(debug=True)
