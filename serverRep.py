#!/usr/bin/env python3
from socket import *
import _thread
import os.path
import sys
from lib.constants import *
import rdt

server = rdt.Socket()
server.bind('localhost', SERVER_PORT)
#print("The server is ready to receive TCP")

#coloque abaixo o diretorio onde esta rodando o codigo, seguido de \\server\\
DATA = os.path.join(FOLDER, "dados.txt")

try:
    os.stat(FOLDER)
except:
    os.mkdir(FOLDER)

try:
    os.stat(FOLDER_CLI)
except:
    os.mkdir(FOLDER_CLI)

arq = open(DATA, 'wb')
arq.close()

def updateFileFolder():
    i = 0
    arq = open(DATA, 'w+')
    filesInFolder = arq.readlines()
    files = os.listdir(FOLDER)
    comp = len(files)

    while i < comp:
        if ((files[i] + '\n') not in filesInFolder): 
            arq.write(files[i] + '\n')
        i = i + 1
        
    arq.close()

def sendToDNS(): #envia dominio e endereco para servidor DNS
    messageDom = DOMAIN_SERVER
    messageAddr = "localhost"

    Clientsocket = socket(AF_INET, SOCK_DGRAM)
    #print("Socket Started")

    Clientsocket.sendto(messageDom.encode('utf-8'), DNS_REP_ADDR)
    print("# Dominio enviado para o servidor DNS")

    Clientsocket.sendto(messageAddr.encode('utf-8'), DNS_REP_ADDR)
    print("# Endereco enviado para o servidor DNS")

    Clientsocket.close()
    #print("Socket Closed")

def handle_client():

    while True:
        msg = server.receive()
        if msg[2] == "checkFiles":
            updateFileFolder()
            #print("\nFiles in your folder:")
            server.send(str(os.path.getsize(DATA)), msg[0], msg[1])
            arq = open(DATA, 'rb')
            
            for line in arq:
                server.send(line.decode('utf8','surrogateescape'), msg[0], msg[1])

            arq.close()

        elif msg[2] == "download":
            fileName = server.receive()[2]
            if (os.path.isfile(os.path.join(FOLDER, fileName))): #verifica se o arquivo que se deseja baixar está contido no servidor
                server.send("exist", msg[0], msg[1])
                server.send(str(os.path.getsize(os.path.join(FOLDER, fileName))), msg[0], msg[1])
                arq = open(os.path.join(FOLDER, fileName), 'rb')
            
                for line in arq:
                    server.send(line.decode('utf8','surrogateescape'), msg[0], msg[1])

                arq.close()

                print ("# Arquivo baixado com sucesso\n")
            else:
                server.send("notExist",msg[0], msg[1])
                print ("# Arquivo nao existe\n")
        elif msg[2] == "socketClose":
            print("Conexão encerrada. Aguardando clientes...")

def main():

    sendToDNS()
    handle_client()
                    
    return  

if __name__ == "__main__":
    main()


