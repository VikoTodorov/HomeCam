from flask import Flask, render_template, request, session, redirect
from flask import *
import database

from user import User


app = Flask(__name__)
app.secret_key = "aOwS(*dsjak,m,EWasd:123aADSjkd"


@app.route('/', endpoint="index")
def index():
    return render_template('index.html')


@app.route('/login')
def return_login():
    return render_template('login.html')


@app.route('/register')
def return_register():
    return render_template('register.html')


@app.route('/register-check', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        if request.form['fname'] != "" and request.form['lname'] != "" and \
        request.form['email'] != "" and request.form['psw'] != "":
            user = User.find_user(request.form['email'])
            if not user:
                values = (None,
                          request.form['fname'],
                          request.form['lname'],
                          request.form['email'],
                          request.form['psw'])
                User(*values).create()
                email = request.form['email']
                session['email'] = email
                return redirect(url_for('homepage'))
            else:
                return render_template('register.html', error="You can't use \
                                       that email")
        else:
            return render_template('register.html', error="You can't use \
                                  that email")


@app.route('/checklogin', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if request.form['email'] != "" and request.form['psw'] != "":
            email = request.form['email']
            password = request.form['psw']
            user = User.find_user(email)
            if not user:
                return render_template("/login.html", error="Invalid email or \
                                       password")
            elif user.verify_pass(password):
                session['email'] = email
                return redirect(url_for('homepage'))
            else:
                return render_template("/login.html", error="Invalid email or \
                                       password")
        else:
            return render_template("/login.html", error="Invalid email or \
                                       password")


@app.route('/homepage', endpoint = "homepage")
def homepage():
    if 'email' in session:
        return render_template('homepage.html')
    else:
        return render_template('index.html')


@app.route('/logout')
def logout():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
