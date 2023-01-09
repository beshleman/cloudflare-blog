#!/usr/bin/env python3

import argparse
import select
import socket
import sys

import signal
import sys
from timeit import default_timer as timer

server = None
start = timer()

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    end = timer()
    elp = end - start
    print("time ", end - start)
    print("got data ", tot)
    print("speed ", tot / elp / 1024 )
    if server is not None:
        server.close()
    s.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser()
parser.add_argument('cid', type=int)
parser.add_argument('port', type=int)
parser.add_argument('type', choices=['dgram', 'seqpacket', 'stream'])
args = parser.parse_args()

# Create a socket
sotype = {
    'dgram': socket.SOCK_DGRAM,
    'seqpacket': socket.SOCK_SEQPACKET,
    'stream': socket.SOCK_STREAM,
}.get(args.type)
s = socket.socket(socket.AF_VSOCK, sotype)

# Bind the socket to the port
server_address = (args.cid, args.port)
s.bind(server_address)
if args.type != 'dgram':
    s.listen(1)

    select.select([s], [], [])
    conn, addr = s.accept()
    server = s
    s = conn


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
