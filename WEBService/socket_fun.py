import select
import socket
import sys
import cv2
import pickle
import numpy as np
import struct


def decrypt(conn, data):
    keys_size = struct.calcsize('LL')
    #data = b''

    while len(data) < keys_size:
        data += conn.recv(4096)

    info = data[:keys_size]
    data = data[keys_size:]

    frame_size = struct.unpack('LL', info)[0]
    key_size = struct.unpack('LL', info)[1]

    while len(data) < frame_size+key_size:
        data += conn.recv(4096)

    frame_data = data[:frame_size]
    key_data = data[frame_size:]
    data = data[frame_size+key_size:]

    frame = pickle.loads(frame_data)
    key = pickle.loads(key_data)

    return frame, key, data
