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
# Append the removed slash
        ndn_name = ndn = "/ndn/handle/" + prefix + "/" + suffix
        print("NDN name from Handle: " + ndn)
        return(ndn)

    def doi2ndn(self):
        name_split = self.pid.split('/', 1)
        prefix = name_split[0].replace(".", "/")
        suffix = name_split[1]
# Append the removed slash
        ndn_name = ndn = "/ndn/doi/" + prefix + "/" + suffix
        print("NDN name from DOI: " + ndn)
        return(ndn)

    def ark2ndn(self):
        pass

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
        print ("from connected  user: " + str(pid))

#Regex should check if handle, doi, or ark is in the link (and not doi:). Also next to this, we do not know what kind of URL are being used within SDC. So where does the pattern matching start?
        regexp_handle = re.compile(r"\b20\.(\d+\.*)+[\/](([^\s\.])+\.*)+\b")
        regexp_doi = re.compile(r"\b10\.(\d+\.*)+[\/](([^\s\.])+\.*)+\b")
# ARK does not work at the moment...
        regexp_ark = re.compile(r"^ark:/([0-9]{5}|[0-9]{9})/([a-z]|[A-Z]|[0-9]|=|#|\\\\*|\\\\+|@|_)+/([a-z]|[A-Z]|[0-9]|=|#|\\\\*|\\\\+|@|_|/|-|\\\\.|%)+$")
# URN: must also match "."
        regexp_urn = re.compile(r"([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9]|-){1,31}:([a-z]|[A-Z]|[0-9]|\\\\(|\\\\)|\\\\+|,|-|\\\\.|:|=|@|;|\\\\$|_|!|\\\\*|'|%([a-f]|[A-F]|[0-9])([a-f]|[A-F]|[0-9]))+$")
        regexp_ndn = re.compile(r"/.*/.*") #WE DONT USE THIS, THE CLIENT DOES NOT GIVE UP A NDN NAME THAT IS THE PLAN, THE CLIENT IS NOT AWARE OF A NDN NETWORK

        pid2ndn = PID2NDN(pid)

        if regexp_handle.match(pid):
            ndn = pid2ndn.handle2ndn()
            print ("sending: " + str(ndn))
            conn.send(ndn.encode())
# Send payload name to client, extracted from JSON metadata for Handle
            pid_metadata = urllib.request.urlopen("http://hdl.handle.net/" + pid + "?locatt=view:json").read()
            output = json.loads(pid_metadata)
            filename = output["name"]
            conn.send(filename.encode())
# Check if NDN name exists in NDN, if yes, send request to NDN and retrieve it
# has to be done

# If not in NDN: Get PID object/payload name to insert it in NDN and sending it to the client directly
            print("Done sending")
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()

        elif regexp_doi.match(pid):
            ndn = pid2ndn.doi2ndn()
            print("DOI")
            ndn = pid2ndn.handle2ndn()
            pidlink = "https://doi.pangaea.de/" + pid + "?format=zip"
            conn.send(pidlink.encode())
# Retrieve filename?
            filename = "pangaeafile.zip"
            conn.send(filename.encode())
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()

        elif regexp_ark.match(pid):
            ndn = pid2ndn.ark2ndn()

        elif regexp_urn.match(pid):
            print("URN")
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

# Send payload name to client, extracted from XML metadata for URN
            conn.send(filename.encode())
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()

        elif regexp_ndn.match(pid):
            ndn = pid2ndn.something2ndn()

if __name__ == "__main__":
    main()
