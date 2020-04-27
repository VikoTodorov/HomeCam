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
    return sock

def getFrame(sock):

    conn, addr = sock.accept()

    data = b''
    payload_size = struct.calcsize("L")

# print(payload_size)
    sock.setblocking(0)
    while True:
        try:
            ready_to_read, ready_to_write, in_error = \
                    select.select([conn,], [conn,], [], 5)
        except select.error:
            conn.shutdown(0)
            conn.close()
        if len(ready_to_read) > 0:
            while len(data) < payload_size:
                data += conn.recv(4096)
            packed_msg_size = data[:payload_size]
            # print(packed_msg_size)

            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            # print(msg_size)

            while len(data) < msg_size:
                data += conn.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame=pickle.loads(frame_data)
            return frame
