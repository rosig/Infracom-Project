#!/usr/bin/env python3
from lib.constants import *
from socket import *
import sys

address =  " "

def menu():
    print("+--------------- Servidor MARE ----------------+")
    print("+------------------ Funcoes -------------------+")
    print("| (1) Solicitar Arquivo                        |")
    print("| (2) Listar Arquivos do Servidor              |")
    print("| (3) Encerrar conexao com o servidor          |")
    print("+----------------------------------------------+\n")

def getOp():
    
    while True:
        op = input("Digite o numero da opcao que deseja: ")
        if op == "1" or op == "2" or op == "3":
            return int(op)
        else:
            print("# A opção digitada não existe\n")

def fileNam():
    fileName = input("Digite o nome do arquivo que deseja baixar:")
    return  fileName

def requestAddressToDNS():
    global address
    message = DOMAIN_SERVER

    Clientsocket = socket(AF_INET, SOCK_DGRAM)
    #print("Socket Started")
    Clientsocket.sendto(message.encode('utf-8'),DNS_CLI_ADDR)
    #print("Requested address to DNS server. Waiting response ....")
    address, addr = Clientsocket.recvfrom(BUFFER_SIZE)
    #print("Server response: ", address)
    Clientsocket.close()
    #print("Socket Closed\n\n")

def tcpServerConection():
    global address
    clientSocket = socket(AF_INET, SOCK_STREAM)
    #print("ConnectionSocket configured! Connecting...")
    clientSocket.connect((address,CLI_REP_PORT))
    #print("ConnectionSocket started!")
    menu()

    while True:

        op = getOp()

        if op == 1:
            clientSocket.send("download".encode('utf-8'))
            fileName = fileNam()
            fileName = fileName.strip()
            clientSocket.send(fileName.encode('utf-8'))
            res = clientSocket.recv(BUFFER_SIZE).decode('utf-8') #resposta de se o arquivo está no servidor
            
            if res == "exist":
                fileSize= int(clientSocket.recv(BUFFER_SIZE))
                arq = open(FOLDER_CLI + fileName, 'wb')
                size = fileSize

                print('\n\nFazendo Download')

                while size > 0:
                    sys.stdout.write('\r')
                    data = clientSocket.recv(1024)
                    size = size - len(data)

                    percentage = (fileSize - size) * 100 / fileSize

                    sys.stdout.write("[%-100s] %d%%" % ('=' * int(percentage), percentage))
                    sys.stdout.flush()
                    arq.write(data)

                arq.close()
                print("\n\n# Download realizado com sucesso!\n")

                menu()

            elif res == "notExist":
                print ("# O arquivo solititado não existe no servidor")

        elif op == 2:
            clientSocket.send("checkFiles".encode('utf-8'))

            fileSize= int(clientSocket.recv(BUFFER_SIZE))
            arq = open(FOLDER_CLI + 'dados.txt', 'wb')
            size = fileSize

            while size > 0:
                    sys.stdout.write('\r')
                    data = clientSocket.recv(1024)
                    size = size - len(data)

                    percentage = (fileSize - size) * 100 / fileSize

                    sys.stdout.write("[%-100s] %d%%" % ('=' * int(percentage), percentage))
                    sys.stdout.flush()
                    arq.write(data)

            print("\n# Lista dos arquivos recebida com sucesso")

            arq.close()

            print("\n\n")
            print("+--------------- Arquivos contidos no servidor ----------------+\n")

            arq = open(FOLDER + 'dados.txt', 'r+')
            filesInFolder = arq.readlines()

            for i in filesInFolder:
                print(i)
    
            arq.close()

            print("+--------------------------------------------------------------+\n")

        else:
            clientSocket.send("socketClose".encode('utf-8'))
            clientSocket.close()
            print("# A conexao com o servidor foi encerrada !\n")
            break


def main():
    requestAddressToDNS()
    tcpServerConection()

if __name__ == "__main__":
    main()