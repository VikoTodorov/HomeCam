import cv2
import numpy as np
import socket
import sys
import pickle
import struct

host = 'https://home-cam.herokuapp.com/' 
port = 8083

cap = cv2.VideoCapture(0)
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsocket.connect((host, port))
while True:
    ret,frame = cap.read()
    data = pickle.dumps(frame)
    clientsocket.sendall(struct.pack("L", len(data)) + data)
