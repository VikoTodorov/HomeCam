import time
import cv2 as cv
from flask_mail import Message

import socket_fun


old_time = 0


def send_mail(mail, app):
    with app.app_context():
        msg = Message("Movement is detected", sender="vikokotest16@gmail.com",
                      recipients=["konstantin.m.donev.2016@elsys-bg.org"])
        msg.body = "Movement was seen on a cam that wasn't supposed to detect any."
        mail.send(msg)


def check(curr_time, mail, app):
    global old_time
    if old_time == 0:
        send_mail(mail, app)
        old_time = curr_time
    elif curr_time - old_time >= 300:
        send_mail(mail, app)
        old_time = curr_time


def generate(sock, expect_move, send_not, mail, app):
    try:
        connect, addr = sock.accept()
        sub = cv.createBackgroundSubtractorMOG2()
        data = b''
        while True:
            frame, key, data = socket_fun.decrypt(connect, data)
            frame = cv.resize(frame, (0,0), fx=0.7, fy=0.7)
            if expect_move: 
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                fgmask = sub.apply(gray)
                kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
                closing = cv.morphologyEx(fgmask, cv.MORPH_CLOSE, kernel)
                opening = cv.morphologyEx(closing, cv.MORPH_OPEN, kernel)
                dilation = cv.dilate(opening, kernel)
                retvalbin, bins = cv.threshold(dilation, 220, 255, cv.THRESH_BINARY)
                contours, hierarchy = cv.findContours(dilation, cv.RETR_EXTERNAL,
                                                      cv.CHAIN_APPROX_SIMPLE)
                minarea = 400
                maxarea = 5000
                for i in range(len(contours)):
                    if hierarchy[0, i, 3] == -1:
                        if send_not:
                            check(time.time(), mail, app)
                        area = cv.contourArea(contours[i])
                        if minarea < area < maxarea:
                            cnt = contours[i]
                            M = cv.moments(cnt)
                            cx = int(M['m10'] / M['m00'])
                            cy = int(M['m01'] / M['m00'])
                            x, y, w, h = cv.boundingRect(cnt)
                            cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

            img = cv.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+img+b'\r\n')
    except BlockingIOError:
        return 'hello'
