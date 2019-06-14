#!/usr/bin/python

import socket

def main():
    host = "145.100.104.119"
    port = 8888

    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    while True:
            data = conn.recv(1024).decode()
            if not data:
                    break
            print ("from connected  user: " + str(data))

            data = str(data)
            print ("sending: " + str(data))
            conn.send(data.encode())

    conn.close()

if __name__ == "__main__":
    main()
