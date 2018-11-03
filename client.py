#!/usr/bin/env python3
from lib.constants import *
from socket import *
address =  " "

def menu():
    print("+--------------- Servidor MARE ----------------+")
    print("+------------------ Funcoes -------------------+")
    print("| (1) Solicitar Arquivo                        |")
    print("| (2) Listar Arquivos do Servidor              |")
    print("| (3) Encerrar conexao com o servidor          |")
    print("+----------------------------------------------+\n")

def getOp():
    op = input("Digite o numero da opcao que deseja: ")
    return op

def fileNam():
    fileName = input("Name of the file you want to download:")
    return  fileName

def requestAddressToDNS():
    global address
    message = DOMAIN_SERVER

    Clientsocket = socket(AF_INET, SOCK_DGRAM)
    print("Socket Started")

    Clientsocket.sendto(message.encode('utf-8'),DNS_CLI_ADDR)
    print("Requested address to DNS server. Waiting response ....")

    address, addr = Clientsocket.recvfrom(BUFFER_SIZE)
    print("Server response: ", address)

    Clientsocket.close()
    print("Socket Closed\n\n")

def tcpServerConection():
    global address

    clientSocket = socket(AF_INET, SOCK_STREAM)
    print("ConnectionSocket configured! Connecting...")

    clientSocket.connect((address,CLI_REP_PORT))
    print("ConnectionSocket started!")

    menu()

    while True:
        i = 0
        op = getOp()

        if op == 1:
            clientSocket.send("download".encode('utf-8'))
            fileName = fileNam()
            clientSocket.send(fileName.encode('utf-8'))
            fileSize= int(clientSocket.recv(BUFFER_SIZE))
            arq = open(FOLDER_CLI + fileName, 'wb')
            size = fileSize

            while size > 0:
                data = clientSocket.recv(1024)
                size = size - len(data)
                arq.write(data)

            arq.close()

        elif op == 2:
            clientSocket.send("checkFiles".encode('utf-8'))
            print("Message Sent! Waiting server response...\n")
            listSize = int(clientSocket.recv(BUFFER_SIZE))

            print("+--------------- Arquivos contidos no servidor ----------------+")

            while i < listSize:
                msg = clientSocket.recv(BUFFER_SIZE)
                msg = msg.decode('utf-8')
                print ("|  " + msg)
                i = i + 1

            print("+--------------------------------------------------------------+\n")

        else:
            clientSocket.close()
            print("A conexao com o servidor foi encerrada !\n")
            #print("Socket Closed")
            break


def main():
    requestAddressToDNS()
    tcpServerConection()

if __name__ == "__main__":
    main()