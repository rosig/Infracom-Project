#!/usr/bin/env python3
from lib.constants import *
from socket import *

domain = ""
address = ""

def recvTranslation():
    global domain
    global address

    serverSocket = socket(AF_INET,SOCK_DGRAM)
    print("# O servidor DNS esta pronto para receber o dominio e endereco do servidor Repositorio")

    serverSocket.bind(('',DNS__REP_PORT))
    domain, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
    address, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
    print("# Dominio e endereco recebidos")         

    return

def sendTranslation():
    global domain
    global address

    serverSocket = socket(AF_INET,SOCK_DGRAM)
    print("# O servidor DNS esta pronto para receber requisicoes de clientes")

    serverSocket.bind(('',DNS_CLI_PORT))
    asking, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)

    if asking == domain:
        serverSocket.sendto(address,clientAddress)
        print("# Endereco enviado com sucesso")     
    else:
        serverSocket.sendto("NoReply",clientAddress)
        print("# O servidor DNS nao tem traducao para o dominio requisitado")

    return


def main():
    recvTranslation()

    while 1:
        sendTranslation()

if __name__ == "__main__":
    main()
