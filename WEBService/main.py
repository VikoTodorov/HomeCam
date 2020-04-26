import time
import datetime

from imutils.video import VideoStream
import imutils
import cv2
import argparse
import threading

from flask import Flask
from flask import render_template, request, redirect, url_for
from flask import session
from flask import Response

from user import User
import database.createdb as database

from HomeCam.WEBService.singlemotiondetector import SingleMotionDetector
import socket_fun

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)
app.secret_key = "aOwS(*dsjak,m,EWasd:123aADSjkd"


def detect_motion(frameCount):
    global outputFrame, lock

    md = SingleMotionDetector(accumWeight=0.1)
    total = 0
    sock = create_socket()
    while True:
        frame = socket_fun.getFrame(sock) 
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        if total > frameCount:
            motion = md.detect(gray)
            if motion is not None:
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                              (0, 0, 255), 2)

        md.update(gray)
        total += 1
        with lock:
            outputFrame = frame.copy()


def generate():
    global outputFrame, lock
    while True:
        with lock:
            if outputFrame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            if not flag:
                continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


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


@app.route('/homepage', endpoint="homepage")
@login_required
def homepage():
    return render_template('app/homepage.html')


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
    return redirect(url_for('index'))


@app.route("/video_feed")
def video_feed():
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    database.createDB()
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())
    t = threading.Thread(target=detect_motion, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()

    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)
