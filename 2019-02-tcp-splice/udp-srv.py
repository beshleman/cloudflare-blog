#!/usr/bin/python

import socket
import sys

import signal
import sys
from timeit import default_timer as timer

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    end = timer()
    elp = end - start
    print("time ", end - start)
    print("got data ", tot)
    print("speed ", tot / elp / 1024 )
    s.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



if len(sys.argv) == 3:
    # Get "IP address of Server" and also the "port number" from
    #argument 1 and argument 2
    ip = sys.argv[1]
    port = int(sys.argv[2])
else:
    print("Run like : python3 server.py <arg1:server ip:this system IP 192.168.1.6> <arg2:server port:4444 >")
    exit(1)

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = (ip, port)
s.bind(server_address)
print("Do Ctrl+c to exit the program !!")

first=True
tot = 0

while True:
#    print("####### Server is listening #######")
    data, address = s.recvfrom(4096)

    if first:
        start = timer()
        first = False
        print("first");
    else:
        tot += len(data)

#    print("\n\n Server received 1 len : ", len(data), "\n\n")
#    print("\n\n Server received  : ", data, "\n\n")
#    data, address = s.recvfrom(4096)
#    print("\n\n Server received 2 len : ", len(data), "\n\n")
#    send_data = input("Type some text to send => ")
#    s.sendto(send_data.encode('utf-8'), address)
#    print("\n\n 1. Server sent : ", send_data,"\n\n")
