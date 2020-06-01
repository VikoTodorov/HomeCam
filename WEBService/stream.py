import time
import datetime

import imutils
import cv2 as cv
import argparse
import threading
import socket_fun
from singlemotiondetector import SingleMotionDetector

def generate(sock, expect_move, send_not):
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

#def detect_motion(conn):
        #frame, key, data = socket_fun.decrypt(conn, data)
        #frame = cv.resize(frame, (0,0), fx=0.5, fy=0.5)
    #    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #    fgmask = sub.apply(gray)
    #    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    #    closing = cv.morphologyEx(fgmask, cv.MORPH_CLOSE, kernel)
    #    opening = cv.morphologyEx(closing, cv.MORPH_OPEN, kernel)
    #    dilation = cv.dilate(opening, kernel)
     #   retvalbin, bins = cv.threshold(dilitaion, 220, 255, cv.THRESH_BINARY)
      #  contours, hierarchy = cv.findContours(dilitaion, cv.RETR_EXTERNEL,
#                                              cv.CHAIN_APPROX_SIMPLE)
       # minarea = 400
        #maxarea = 5000
        #for i in range(len(contours)):
          #  if hierarchy[0, i, 3] == -1:
         #       area = cv.contourArea(contours[i])
           #     if minarea < area < maxarea:
             #       cnt = contours[i]
            #        M = cv.moments(cnt)
              #      cx = int(M['m10'] / M['m00'])
                #    cy = int(M['m01'] / M['m00'])
               #     x, y, w, h = cv.boundingRect(cnt)
                 #   cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
                  #  cv.putText(image, str(cx) + "," +str(cy), (cx+10, cy+10),
                    #           cv.FONT_HERSHEY_SIMPLEX,0.3, (0,0,255), 1)
                    #cv.drawMarker(frame, (cx, cy), (0, 255, 255),
                     #             cv.MARKER_CROSS, markerSize=8, thickness=3,
                      #            line_type=cv.LINE_8)'''
        #img = cv.imencode('.jpg', frame)[1].tobytes()
        #yield (b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+img+b'\r\n')

