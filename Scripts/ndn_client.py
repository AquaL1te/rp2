#!/usr/bin/python

import socket
import re
import urllib3
import os

def send_pid(host, port, pid):
# Open socket to GW and send PID (can be all kinds of PID types that the GW has implemented)
    mySocket = socket.socket()
    mySocket.connect((host,port))
    mySocket.send(pid.encode())

# Receive NDN name and filename of the payload
    ndnname = mySocket.recv(1024).decode()
    print(ndnname)
    if ndnname == "Please provide one of the following PID types: Handle, DOI or URN":
        print("No correct PID type is provided")
        return

    filename = mySocket.recv(1024).decode()
    print(filename)
    mySocket.close()
    print("Connection closed")

# Request object from NDN network
    cmd = 'ndncatchunks ' + ndnname + ' > ' + filename
    os.system(cmd)

def main():
        host = "ndn-producer-1.ndn.default.svc.cluster.local"
        port = 8889
        pid = input("Please enter a pid (Handle, DOI or URN): ")
        send_pid(host, port, pid)

if __name__ == "__main__":
        main()

