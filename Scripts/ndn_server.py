#!/usr/bin/python

import socket
import re
import urllib3
import urllib.request
import json
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import ssl
from xml.dom import minidom

class PID2NDN(object):
    def __init__(self, pid):
        self.pid = pid

    def handle2ndn(self):
        name_split = self.pid.split('/', 1)
        prefix = name_split[0].replace(".", "/")
        suffix = name_split[1]
        ndn_name = ndn = "/ndn/handle/" + prefix + "/" + suffix
        print("NDN name from Handle: " + ndn)
        return(ndn)

    def doi2ndn(self):
        name_split = self.pid.split('/', 1)
        prefix = name_split[0].replace(".", "/")
        suffix = name_split[1]
        ndn_name = ndn = "/ndn/doi/" + prefix + "/" + suffix
        print("NDN name from DOI: " + ndn)
        return(ndn)

    def urn2ndn(self):
        prefix = self.pid.replace(":", "/")
        ndn_name = ndn = "/ndn/urn/" + prefix
        print("NDN name from URN: " + ndn)
        return(ndn)

    def something2ndn(self):
        pass

def main():
    host = "ndn-producer-1.ndn.default.svc.cluster.local"
    port = 8889

    s = socket.socket()
    s.bind((host,port))
    s.listen(1)

    while True:
        print("Waiting for client")
        conn, addr = s.accept()
        print ("Connection from: " + str(addr))
        piddata = conn.recv(1024).decode()
        pid = str(piddata)
        print ("PID from connected user: " + str(pid))

# Pattern matching: Regex should check if handle, doi, or urn is in the link. We do not know what kind of web resolvers are being used within a data infrastructure, but most web resolver incorporate the PID type in the URL.
        regexp_handle = re.compile(r"\b20\.(\d+\.*)+[\/](([^\s\.])+\.*)+\b")
        regexp_doi = re.compile(r"\b10\.(\d+\.*)+[\/](([^\s\.])+\.*)+\b")
# URN: must also match "."
        regexp_urn = re.compile(r"([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9]|-){1,31}:([a-z]|[A-Z]|[0-9]|\\\\(|\\\\)|\\\\+|,|-|\\\\.|:|=|@|;|\\\\$|_|!|\\\\*|'|%([a-f]|[A-F]|[0-9])([a-f]|[A-F]|[0-9]))+$")

        pid2ndn = PID2NDN(pid)

        if regexp_handle.match(pid):
            ndn = pid2ndn.handle2ndn()
            print("PID type: Handle")
            print ("sending: " + str(ndn))
            conn.send(ndn.encode())

            pid_metadata = urllib.request.urlopen("http://hdl.handle.net/" + pid + "?locatt=view:json").read()
            output = json.loads(pid_metadata)
            filename = output["name"]
            conn.send(filename.encode())
            print("Done sending")
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()

        elif regexp_doi.match(pid):
            ndn = pid2ndn.doi2ndn()
            print("PID type: DOI")
            ndn = pid2ndn.handle2ndn()
            pidlink = "https://doi.pangaea.de/" + pid + "?format=zip"
            conn.send(pidlink.encode())
            filename = "pangaeafile.zip"
            conn.send(filename.encode())
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()

        elif regexp_urn.match(pid):
            print("PID type: URN")
            ndn = pid2ndn.urn2ndn()
            print ("sending: " + str(ndn))
            conn.send(ndn.encode())

# For URN for this PID provider, we need to extract the identifier, as this needs to be used twice for metadata (e.g.:anp:anp:).
            get_urn_identity = pid.split(':', 1)
            urn_identity = get_urn_identity[0]
            pid_metadata = urllib.request.urlopen("http://services.kb.nl/mdo/oai?verb=GetRecord&identifier=" + urn_identity + ":" + pid + "&metadataPrefix=didl")
            xmldoc = minidom.parse(pid_metadata)
            pid_metadata.close()
            val = xmldoc.getElementsByTagName('didl:Resource')[1].toxml()
            pattern='(ref=")(.*)(")'
            g=re.search(pattern,val)
            filename = (g.group(2))
            conn.send(filename.encode())
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()

        else:
            message = "Please provide one of the following PID types: Handle, DOI or URN"
            conn.send(message.encode())
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()

if __name__ == "__main__":
    main()

