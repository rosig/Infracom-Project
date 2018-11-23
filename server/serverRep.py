#!/usr/bin/env python3
from socket import *
from lib import libServer as svr
import _thread
import os.path
import sys
from lib.constants import *

server = svr.TCPServerSocket()
#print("The server is ready to receive TCP")

#coloque abaixo o diretorio onde esta rodando o codigo, seguido de \\server\\
DATA = os.path.join(FOLDER, "dados.txt")

try:
    os.stat(FOLDER)
    os.stat(FOLDER_CLI)
    arq = open(DATA, 'wb')
    arq.close()
except:
    os.mkdir(FOLDER)
    os.mkdir(FOLDER_CLI)
    arq = open(DATA, 'wb')
    arq.close()
    #print("Uma pasta para os clientes e uma pasta para o servidor foram criadas")

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

def handle_client(index):

    while True:
        msg = server.recvMessage(index)
        if msg == "checkFiles":
            updateFileFolder()
            #print("\nFiles in your folder:")

            server.sendMessage((str(os.path.getsize(DATA))), index)
            arq = open(DATA, 'rb')
            
            for line in arq:
                server.connectedSockets[index].send(line)

            arq.close()

        elif msg == "download":
            fileName = server.recvMessage(index)
            if (os.path.isfile(os.path.join(FOLDER, fileName))): #verifica se o arquivo que se deseja baixar está contido no servidor
                server.sendMessage("exist",index)
                server.sendMessage((str(os.path.getsize(os.path.join(FOLDER, fileName)))), index)
                arq = open(os.path.join(FOLDER, fileName), 'rb')
            
                for line in arq:
                    server.connectedSockets[index].send(line)

                arq.close()

                print ("# Arquivo baixado com sucesso\n")
            else:
                server.sendMessage("notExist",index)
                print ("# Arquivo nao existe\n")

        elif msg == "socketClose":
            print("# A conexão com o cliente de index ",index," foi encerrada")
def main():

    sendToDNS()
    while True:
        index = server.acceptConnection()
        num = _thread.start_new_thread(handle_client, (index,))
                    
    return  

if __name__ == "__main__":
    main()


