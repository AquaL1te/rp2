#!/usr/bin/python

import socket
import re
import urllib3
import os

def send_pid(host, port, pid):
# Open socket to GW and send PID (can be all kinds of PID types that the GW knows of)
    mySocket = socket.socket()
    mySocket.connect((host,port))
    mySocket.send(pid.encode())

# Receive NDN name and filename of the payload
    ndnname = mySocket.recv(1024).decode()
    print(ndnname)
    filename = mySocket.recv(1024).decode()
    print(filename)
    mySocket.close()
    print("Connection closed")

# Misschien hier toch de filename mee terugsturen dmv socket ipv ndnpeek en ndnpoke
# Request object from NDN network
    cmd = 'ndncatchunks ' + ndnname + ' > ' + filename
    os.system(cmd)

def main():
        host = "ndn-producer-1.ndn.default.svc.cluster.local"
        port = 8889
        pid = input("Please enter a pid: ")
        send_pid(host, port, pid)

if __name__ == "__main__":
        main()
