#!/home/ruslan/anaconda3/bin/python

import socket
import sys
import time

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("", 10001))
    sock.send(bytes(sys.argv[1], encoding='UTF-8'))
    data = sock.recv(2048)
    print(data.decode("utf-8"))
        
except ConnectionResetError:
    data = client.recv(2048)
    print(data.decode("utf-8"))
    exit(0)
