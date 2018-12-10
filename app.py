from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)

@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Login Sukses"

@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    if request.form['username'] == 'admin' and request.form['password'] == 'admin':
        session['logged_in'] = True
    else:
        flash('Wrong Username / Password')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
