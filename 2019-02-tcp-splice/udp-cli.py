#!/usr/bin/python3

import socket
import sys

if len(sys.argv) == 3:
    # Get "IP address of Server" and also the "port number" from argument 1 and argument 2
    ip = sys.argv[1]
    port = int(sys.argv[2])
else:
    print("Run like : python3 client.py <arg1 server ip 192.168.1.102> <arg2 server port 4444 >")
    exit(1)

# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
print("Do Ctrl+c to exit the program !!")

# Let's send data through UDP protocol
while True:
#    send_data = input("Type some text to send =>");
    send_data =  b"0" * (1 * 1024)
#    s.sendto(send_data.encode('utf-8'), (ip, port))
    ret = s.sendto(send_data, (ip, port))
    print("\n\n 1. Client Sent ret : ", ret, "\n\n")
    ret = s.sendto(send_data, (ip, port))
    print("\n\n 2. Client Sent ret : ", ret, "\n\n")
    data, address = s.recvfrom(4096)
    print("\n\n 3. Client received len: ", len(data.decode), "\n\n")
# close the socket
s.close()

