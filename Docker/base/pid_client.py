#!/usr/bin/python

import socket
import re
import urllib3
import datetime
import urllib.request

def send_pid(host, port, pid):
# Open socket to GW and send PID (can be all kinds of PID types that the GW knows of)
    mySocket = socket.socket()
    mySocket.connect((host,port))
    mySocket.send(pid.encode())

# Receive PID server object link and filename of the payload
    pidlink = mySocket.recv(1024).decode()
    print(pidlink)
    filename = mySocket.recv(1024).decode()
    print(filename)

# Request the file and benchmark the time it takes to receive the file (TCP?)
    start = datetime.datetime.now()
    urllib.request.urlretrieve(pidlink, filename)
    end = datetime.datetime.now()
    c = end - start
    print(str(c.total_seconds() * 1000) + " milliseconds")
    print("Successfully get the file")
    mySocket.close()
    print("Connection closed")

def main():
        host = "ndn-producer-1.ndn.default.svc.cluster.local"
        port = 8888
        pid = input("Please enter a pid:")
        send_pid(host, port, pid)

if __name__ == "__main__":
        main()
