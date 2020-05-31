import time
import datetime

import imutils
import cv2
import argparse
import threading
import socket_fun
import socket_fun
from singlemotiondetector import SingleMotionDetector

outputFrame = None
lock = threading.Lock()

def detect_motion(frameCount):
    global outputFrame, lock

    md = SingleMotionDetector(accumWeight=0.1)
    total = 0
    sock, conn, addr = socket_fun.create_socket()
    while True:
        frame = socket_fun.getFrame(sock, conn)
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
