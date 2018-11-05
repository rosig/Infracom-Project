#!/usr/bin/env python3
from lib.constants import *
from socket import *

domain = ""
address = ""

def recvTranslation():
    global domain
    global address

    serverSocket = socket(AF_INET,SOCK_DGRAM)
    print("The serverDNS is ready to receive domain and address from ServerRepository")

    serverSocket.bind(('',DNS__REP_PORT))
    domain, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
    address, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
    print("Domain and address received")         

    return

def sendTranslation():
    global domain
    global address

    serverSocket = socket(AF_INET,SOCK_DGRAM)
    print("The serverDNS is ready to receive requests from Client")

    serverSocket.bind(('',DNS_CLI_PORT))
    asking, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)

    if asking == domain:
        serverSocket.sendto(address,clientAddress)
        print("Address sent successfully")     
    else:
        serverSocket.sendto("NoReply",clientAddress)
        print("No translation for the requested domain")

    return


def main():
    recvTranslation()

    while 1:
        sendTranslation()

if __name__ == "__main__":
    main()
