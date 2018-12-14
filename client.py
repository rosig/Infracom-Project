#!/usr/bin/env python3
from lib.constants import *
from socket import *
import sys
import rdt

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

def rdtServerConection():
    global address
    client = rdt.Socket()
    client.bind('localhost', CLI_REP_PORT)
    menu()

    while True:

        op = getOp()

        if op == 1:
            client.send("download", address, SERVER_PORT)
            fileName = fileNam()
            fileName = fileName.strip()
            client.send(fileName, address, SERVER_PORT)
            res = client.receive()[2] #resposta de se o arquivo está no servidor
            
            if res == "exist":
                fileSize= int(client.receive()[2])
                arq = open(os.path.join(FOLDER_CLI, fileName), 'wb')
                size = fileSize

                print('\n\nFazendo Download')

                while size > 0:
                    sys.stdout.write('\r')
                    data = client.receive()[2]
                    size = size - len(data)

                    percentage = (fileSize - size) * 100 / fileSize

                    sys.stdout.write("[%-100s] %d%%" % ('=' * int(percentage), percentage))
                    sys.stdout.flush()
                    arq.write(bytes(data, 'utf-8'))

                arq.close()
                print("\n\n# Download realizado com sucesso!\n")

                menu()

            elif res == "notExist":
                print ("\n# O arquivo solicititado não existe no servidor\n")

        elif op == 2:
            client.send("checkFiles", address, SERVER_PORT)

            fileSize= int(client.receive()[2])
            arq = open(os.path.join(FOLDER_CLI, 'dados.txt'), 'wb')
            size = fileSize

            while size > 0:
                sys.stdout.write('\r')
                data = client.receive()[2]
                size = size - len(data)
                
                percentage = (fileSize - size) * 100 / fileSize

                sys.stdout.write("[%-100s] %d%%" % ('=' * int(percentage), percentage))
                sys.stdout.flush()
                arq.write(bytes(data, 'utf-8'))

            print("\n# Lista dos arquivos recebida com sucesso")

            arq.close()

            print("\n\n")
            print("+--------------- Arquivos contidos no servidor ----------------+\n")

            arq = open(os.path.join(FOLDER, 'dados.txt'), 'r+')
            filesInFolder = arq.readlines()

            for i in filesInFolder:
                print(i)
    
            arq.close()

            print("+--------------------------------------------------------------+\n")

        elif op == 3:
            client.send("socketClose", address, SERVER_PORT)
            client.unbind()
            print("# A conexao com o servidor foi encerrada !\n")
            break

def main():
    requestAddressToDNS()
    rdtServerConection()

if __name__ == "__main__":
    main()
