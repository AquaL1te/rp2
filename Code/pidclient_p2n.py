#!/usr/bin/python

import socket
import re
import urllib3


class PID2NDN(object):
    def __init__(self, pid):
        self.pid = pid


    def handle2ndn(self):
        """
        Not sure why you use 'old' and 'new' variable names,
        if you don't need the vars after conversion,
        you can overwrite them as well :)
        """
        name_split = self.pid.split('/', 1)
        name_1_old = self.pid.split[0]
        name_2 = name_split[1]
        name_1_new = name_1_old.replace(".", "/")
        #Append the removed slash
        ndn = "/ndn/handle/" + name_1_new + "/" + name_2
        print("NDN name from Handle: " + ndn)
        return(ndn)


    def something2ndn(self):
        pass


def main():
        host = "145.100.104.119"
        port = 8888

        pid = input("Please enter an pid:")

        regexp_handle = re.compile(r"\b(\d+\.*)+[\/](([^\s\.])+\.*)+\b")
        regexp_ndn = re.compile(r"/.*/.*")

        pid2ndn = PID2NDN(pid)

        if regexp_handle.match(pid):
            ndn = pid2ndn.handle2ndn()
        elif regexp_ndn.match(pid):
            ndn = pid2ndn.something2ndn()

        mySocket = socket.socket()
        mySocket.connect((host,port))
        mySocket.send(ndn.encode())
        data = mySocket.recv(1024).decode()
        mySocket.close()

if __name__ == "__main__":
    main()
