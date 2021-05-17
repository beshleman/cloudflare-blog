#!/usr/bin/python3

import socket
import sys

if len(sys.argv) == 4:
    path = sys.argv[1]
    ip = sys.argv[2]
    port = int(sys.argv[3])
else:
    print("Run like : python3 client.py <arg1 path /s1> <arg2 ip> <arg3 port>")
    exit(1)

# Create socket for unix
s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM, 0)
print("Do Ctrl+c to exit the program !!")

# Let's send data through UDP protocol
#    send_data = input("Type some text to send =>");
send_data = b"hello from client\n";
#send_data =  b"1" * (1 * 1024)
#    s.sendto(send_data.encode('utf-8'), (ip, port))
ret = s.sendto(send_data, path)
print("\n\n 1. UNix Client Sent ret : ", ret, "\n\n")
#ret = s.sendto(send_data, path)
#print("\n\n 2. Client Sent ret : ", ret, "\n\n")


# Create a UDP socket
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = (ip, port)
s2.bind(server_address)

data, address = s2.recvfrom(4096)
print("\n\n UDP Server received 1 len : ", len(data), "\n\n")
print("\n\n UDP Server received 1 : ", data, "\n\n")

# close the socket
s.close()
s2.close()

