import argparse
import socket
import threading

from flask import Flask
from flask import render_template, request, redirect, url_for
from flask import session
from flask import Response
from flask_mail import Mail

from user import User
import database.createdb as database
import socket_fun
import cv2 as cv

from WEBService.stream import detect_motion, set_flag

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'donev.konstantin@gmail.com'
app.config['MAIL_PASSWORD'] = 'oodsgwocbkbokoif'
mail = Mail(app)
app.secret_key = "aOwS(*dsjak,m,EWasd:123aADSjkd"

lock = threading.Lock()
sock = socket.socket()
host = socket.gethostname()
port = 9999

sock.bind((host,port))
sock.listen(5)
sock.setblocking(0)


@app.route('/', endpoint="index")
def index():
    if 'email' in session:
        return redirect(url_for('homepage'))
    return render_template('app/index.html')


@app.route('/register', methods=['GET', 'POST'], endpoint="register")
def register():
    database.createDB()
    if request.method == 'GET':
        return render_template('auth/register.html')

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
                return render_template('auth/register.html', error="You can't use \
                                       that email")
        elif request.form['fname'] == "":
            return render_template('auth/register.html', error="First name\
                                  is required")
        elif request.form['lname'] == "":
            return render_template('auth/register.html', error="Last name\
                                  is required")
        elif request.form['email'] == "":
            return render_template('auth/register.html', error="Email\
                                  is required")
        elif request.form['psw'] == "":
            return render_template('auth/register.html', error="Password\
                                  is required")


@app.route('/login', methods=['GET', 'POST'], endpoint="login")
def login():
    database.createDB()
    if request.method == 'GET':
        return render_template('auth/login.html')

    elif request.method == 'POST':
        if request.form['email'] != "" and request.form['psw'] != "":
            email = request.form['email']
            password = request.form['psw']
            user = User.find_user(email)
            if not user:
                return render_template("auth/login.html", error="Invalid email or \
                                       password")
            elif user.verify_pass(password):
                session['email'] = email
                return redirect(url_for('homepage'))
            else:
                return render_template("auth/login.html", error="Invalid email or \
                                       password")
        else:
            return render_template("auth/login.html", error="Invalid email or \
                                       password")


def login_required(fun):
    #  @functools.wraps(fun)
    def wrapped_fun(**kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return fun(**kwargs)

    return wrapped_fun


@app.route('/homepage', methods=['GET', 'POST'], endpoint="homepage")
@login_required
def homepage():
#    try:
#        connect, addr = sock.accept()
#        globals()['conn'] = connect
#        return render_template('app/homepage.html', flag = True)
#    except BlockingIOError:
#        return render_template('app/homepage.html', flag = False)

#        connect, addr = sock.accept()
#        globals()['conn'] = connect
    if request.method == 'POST':
        set_flag(False)
        return render_template("app/no_mov_expected.html")
    else:
        return render_template('app/homepage.html')


@app.route("/no_mov_exp", methods=['GET', 'POST'], endpoint="no_mov_exp")
def no_mov():
    if request.method == 'POST':
        set_flag(True)
        return render_template("app/homepage.html")
    else:
        return render_template("app/no_mov_expected.html")


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
    return redirect(url_for('index'))


def generate():
    try:
        connect, addr = sock.accept()
        data = b''
        while True:
            frame, key, data = socket_fun.decrypt(connect, data) 
            frame = cv.resize(frame, (0,0), fx=0.7, fy=0.7)
            img = cv.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+img+b'\r\n')
    except BlockingIOError:
        return 'hello'


@app.route("/video_feed")
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    database.createDB()
    t = threading.Thread(target=detect_motion, args=(32, , mail, app))
    t.daemon = True
    t.start()
    app.run(host='127.0.0.1', debug=True, threaded=True, use_reloader=False)

