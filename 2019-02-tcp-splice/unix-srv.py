#!/usr/bin/python

import socket
import sys
import os

if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    print("Run like : python3 server.py <arg1:server /tmp/s1>")
    exit(1)

# Make sure the socket does not already exist
try:
    os.unlink(path)
except OSError:
    if os.path.exists(path):
        raise

# Create a UDP socket
s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
# Bind the socket to the port
#server_address = (ip, port)
s.bind(path)
print("Do Ctrl+c to exit the program !!")

#s.connect(path)

while True:
    print("####### Server is listening #######")
    data, addr = s.recvfrom(1024*8)
    print("\n\n Server received 1 len : ", len(data), "\n\n")
    print("\n\n Server received addr : ", addr, "\n\n")

    data = s.recv(4096)
    print("\n\n Server received 2 len : ", len(data), "\n\n")
    send_data = input("Type some text to send => ")
    s.sendto(send_data.encode('utf-8'), path)
    print("\n\n 1. Server sent : ", send_data,"\n\n")
