from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, jsonify, send_file
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from Auth_Model import *
from Users_Model import *
import os

# from flask_autoindex import AutoIndex 


app = Flask(__name__)
users_list = Users_Model()
UPLOAD_FOLDER = os.path.dirname(os.getcwd())+'/user' #ganti ini pake directory kalian
USER_UPLOAD_FOLDER = os.path.dirname(os.getcwd()) #ganti ini pake directory kalian
CURRENT_WORKING_DIRECTORY = ''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3'])
app.config['USER_UPLOAD_FOLDER'] = USER_UPLOAD_FOLDER

a_model = Auth_Model()
activeToken = '' #globalVariableforToken
Bootstrap(app)

def printToken():
    if activeToken == '':
        return None
    elif not authenticate(activeToken):
        return None
    else:
        return activeToken


def authenticate(checkedToken):
    flag_authorized = a_model.cek_token(checkedToken)
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

def append_dir(current,path):
    result = current+'/'+path
    
    return result
    
def pop_dir(current):
    pisah = current.split('/')
    pisah.pop()
    pisah = iter(pisah)
    next(pisah)
    hasil=''
    for i in pisah:
        hasil = hasil+'/'+i
    
    return hasil


def list_list(path):
    list_of_user = {
        'files':[],
        'folder':[]
    }
    folders=[]
    file=[]
    semua=[]
    files = os.listdir(path)
    for a in files:
        semua.append(a)
    
    for i in files:
        if os.path.isdir(path+'/'+i):
            list_of_user['folder'].append(i)
            # folders.append(i)
        elif os.path.isfile(path+'/'+i):
            list_of_user['files'].append(i)
            # file.append(i)
    
    return list_of_user

def get_size(start_path = USER_UPLOAD_FOLDER ):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

@app.route("/")
def home():
    if not authenticate(activeToken):
        return redirect('/login')
    else:
        # return render_template('home.html', filelist=make_tree(USER_UPLOAD_FOLDER))
        size = get_size(start_path=CURRENT_WORKING_DIRECTORY)
        size = sizeof_fmt(size)
        return render_template('home.html', filelist=list_list(CURRENT_WORKING_DIRECTORY), current=CURRENT_WORKING_DIRECTORY, size=size)

@app.route('/home', methods=['GET'])
def home_list():
    current = request.args.get('current_dir')
    folder = request.args.get('folder')
    size = get_size(start_path=CURRENT_WORKING_DIRECTORY)
    size = sizeof_fmt(size)
    path_current=append_dir(current,folder)
    return render_template('home.html', filelist=list_list(path_current), current=path_current, size=size)
    # a = path_current
    # a = jsonify(a)
    # return a

@app.route("/token")
def mytoken():
    return printToken()

@app.route("/cektoken/<token>")
def mytoktoken(token):
    if authenticate(token):
        return 'token benar'
    else:
        return 'token salah'

@app.route('/login', methods=['GET', 'POST'])
def login():
    global USER_UPLOAD_FOLDER
    global CURRENT_WORKING_DIRECTORY
    global activeToken
    if request.method == 'POST':
        if users_list.login(request.form['username'], request.form['password']):
            USER_UPLOAD_FOLDER = UPLOAD_FOLDER + '/' + request.form['username']
            app.config['USER_UPLOAD_FOLDER'] = USER_UPLOAD_FOLDER
            CURRENT_WORKING_DIRECTORY = USER_UPLOAD_FOLDER
            activeToken = a_model.get_token(request.form['username'], users=users_list)
            flash('OK', 'success')
            return redirect('/')
        else:
            flash('Wrong Username / Password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    global USER_UPLOAD_FOLDER
    if request.method == 'POST':
        if users_list.add(request.form['username'], request.form['password']):
            flash('Create Account Success !', 'success')
#            session['logged_in'] = True
            USER_UPLOAD_FOLDER = UPLOAD_FOLDER + '/' + request.form['username']
            if not os.path.exists(USER_UPLOAD_FOLDER):
                os.makedirs(USER_UPLOAD_FOLDER)
            app.config['USER_UPLOAD_FOLDER'] = USER_UPLOAD_FOLDER
            return redirect('/')
        else:
            flash('Username Already Exist !', 'error')
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    global activeToken
    global CURRENT_WORKING_DIRECTORY
    activeToken = ''
    CURRENT_WORKING_DIRECTORY = ''
    return redirect('/')

@app.route("/upload")
def upload():
    if not authenticate(activeToken):
        return redirect('/login')
    else:
        return render_template('upload.html')

@app.route("/uploader", methods=['POST'])
def uploader():
    current = request.form.get('current_dir')
    size = get_size(start_path=CURRENT_WORKING_DIRECTORY)
    size = sizeof_fmt(size)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template('home.html', filelist=list_list(current), current=current, size=size)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return render_template('home.html', filelist=list_list(current), current=current, size=size)
        #if
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = filename.replace("_", " ")
            uploadedPath = current + '/' + filename
            file.save(uploadedPath)
            size = get_size(start_path=CURRENT_WORKING_DIRECTORY)
            size = sizeof_fmt(size)
#            return redirect(url_for('uploaded_file',
#                                    filename=filename))
            return render_template('home.html', filelist=list_list(current), current=current, size=size)

    else:
        return render_template('home.html', filelist=list_list(current), current=current, size=size)

@app.route('/download')
def download():
    current = request.args.get('current_dir')
    file = request.args.get('file')
    path_to_download = current + '/' + file
    return send_file(path_to_download, attachment_filename=file, as_attachment=True)

@app.route('/open')
def open():
    current = request.args.get('current_dir')
    file = request.args.get('file')
    path_to_download = current + '/' + file
    return send_file(path_to_download, attachment_filename=file, as_attachment=False)

@app.route('/makedir', methods=['POST'])
def make_dir():
    size = get_size(start_path=CURRENT_WORKING_DIRECTORY)
    size = sizeof_fmt(size)
    current = request.form.get('current_dir')
    directory = request.form.get('folder')
    folder = current+'/'+directory
    if not os.path.exists(folder):
        os.makedirs(folder)
    return render_template('home.html', filelist=list_list(current), current=current, size=size)

@app.route('/uproot', methods=['GET'])
def uproot():
    current = request.args.get('current_dir')
    size = get_size(start_path=CURRENT_WORKING_DIRECTORY)
    size = sizeof_fmt(size)
    path_current = pop_dir(current)
    return render_template('home.html', filelist=list_list(path_current), current=path_current, size=size)

@app.route('/delete', methods=['GET'])
def delete_file():
    current = request.args.get('current_dir')
    deletedObject = request.args.get('object')
    path_to_delete = current + '/' + deletedObject
    if os.path.exists(path_to_delete):
        if os.path.isdir(path_to_delete):
            os.rmdir(path_to_delete)
        else:
            os.remove(path_to_delete)
        size = get_size(start_path=CURRENT_WORKING_DIRECTORY)
        size = sizeof_fmt(size)
        return render_template('home.html', filelist=list_list(current), current=current, size=size)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #max upload 16 mb
    app.run(debug=True, host='0.0.0.0')
