#!/usr/bin/python3

import socket
import sys
import os

if len(sys.argv) == 4:
    path = sys.argv[1]
    ip = sys.argv[2]
    port = int(sys.argv[3])
else:
    print("Run like : python3 server.py <arg1 path /s1> <arg2 ip> <arg3 port>")
    exit(1)

# Make sure the socket does not already exist
try:
    os.unlink(path)
except OSError:
    if os.path.exists(path):
        raise


# Create a UDP socket srv
s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
# Bind the socket to the port
#server_address = (ip, port)
s.bind(path)
print("Do Ctrl+c to exit the program !!")

print("####### unix Server is listening #######")
data, addr = s.recvfrom(1024*8)
#print("\n\n Server received 1 len : ", len(data), "\n\n")
print("\n\n unix Server received  : ", data, "\n\n")


# Create socket for unix cli
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

ret = s2.sendto(data, (ip, port))
print("\n\n 1. udp Client Sent ret : ", ret, "\n\n")

# close the socket
s.close()
s2.close()
