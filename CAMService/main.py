import cv2
import numpy as np
import socket
import sys
import pickle
import struct

host = socket.gethostname()
port = 9999

cap = cv2.VideoCapture(0)
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

P_key = input('Enter your key: ')
P_key = pickle.dumps(P_key)
clientsocket.connect((host, port))
while True:
    ret,frame = cap.read()
    data = pickle.dumps(frame)
    clientsocket.sendall(struct.pack("LL", len(data), len(P_key)) + data + P_key)
