import threading
import time

import cv2
import imutils
from singlemotiondetector import SingleMotionDetector
from flask import current_app
from flask_mail import Message


outputFrame = None
lock = threading.Lock()
movementFlag = True


def send_mail(mail, app):
    with app.app_context():
        msg = Message("Movement is detected", sender="donev.konstantin@gmail.com",
                      recipients=["konstantin.m.donev.2016@elsys-bg.org"])
        msg.body = "Movement was seen on a cam that wasn't supposed to detect any."
        mail.send(msg)


old_time = 0


def check(curr_time, mail, app):
    global old_time
    if old_time == 0:
        send_mail(mail, app)
        old_time = curr_time
    elif curr_time - old_time >= 300:
        send_mail(mail, app)


def set_flag(flag):
    global movementFlag
    movementFlag = flag


def detect_motion(frameCount, vs, mail, app):
    global outputFrame, lock
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=1000)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        if total > frameCount:
            motion = md.detect(gray)
            if motion is not None:
                if not movementFlag:
                    check(time.time(), mail, app)
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