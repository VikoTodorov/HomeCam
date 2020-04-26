import select
import socket
import sys
import cv2
import pickle
import numpy as np
import struct

def create_socket():
    host = socket.gethostname()
    port = 8083

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((host, port))
    sock.listen(10)
    
