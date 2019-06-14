import socket
import re
import urllib3

name = input("Please enter an object name:")

def testname(name):
#       global nametype
        if re.match(r"\b(\d+\.*)+[\/](([^\s\.])+\.*)+\b", name):
                nametype = "handle"
                print("Handle")
        elif re.match(r"/.*/.*", name):
                nametype = "ndn"
                print("NDN")
        else:
                nametype = "Unrecognized"

if nametype == "handle":
        name_split = name.split('/', 1)
        name_1_old = name_split[0]
        name_2 = name_split[1]
        name_1_new = name_1_old.replace(".", "/")
#Append the removed slash
        ndn_new = "/ndn/handle/" + name_1_new + "/" + name_2
        print("NDN name from Handle:" + ndn_new)

def Main():
        host = '145.100.104.119'
        port = 8888

        mySocket = socket.socket()
        mySocket.connect((host,port))

        message = ndn_new

        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()
#
#                print ('Received from server: ' + data)
#
#                message = input(" -> ")

        mySocket.close()

if __name__ == '__main__':
    Main()

