#!/usr/bin/python3

import socket
import sys
import time

if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    print("Run like : python3 client.py <arg1 path /tmp/unixsock1>")
    exit(1)

# Create socket for server
s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM, 0)
print("Do Ctrl+c to exit the program !!")

send_data =  b"0" * (4 * 1024)
# Let's send data through UDP protocol
while True:
#    send_data = input("Type some text to send =>");
#    send_data = b"hello from client\n";
#    send_data =  b"1" * (1 * 1024)
#    s.sendto(send_data.encode('utf-8'), (ip, port))
    ret = s.sendto(send_data, path)
    time.sleep(1/1000000.0)
#    break
#    print("\n\n 1. Client Sent ret : ", ret, "\n\n")
#    ret = s.sendto(send_data, path)
#    print("\n\n 2. Client Sent ret : ", ret, "\n\n")
#    data = s.recvfrom(4096)
#    print("\n\n 3. Client received len: ", len(data.decode), "\n\n")
# close the socket
s.close()

