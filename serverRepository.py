#!/usr/bin/env python3
from socket import *
from lib import libServer as svr
import _thread
import os.path
import sys
from lib.constants import *

server = svr.TCPServerSocket()
print("The server is ready to receive TCP")

#coloque abaixo o diretorio onde esta rodando o codigo, seguido de \\server\\

try:
    os.stat(FOLDER)
    os.stat(FOLDER_CLI)
except:
    os.mkdir(FOLDER)
    os.mkdir(FOLDER_CLI)
    print("Uma pasta para os clientes e uma pasta para o servidor foram criadas")

def sendToDNS(): #envia dominio e endereco para servidor DNS
    messageDom = DOMAIN_SERVER
    messageAddr = "localhost"

    Clientsocket = socket(AF_INET, SOCK_DGRAM)
    print("Socket Started")

    Clientsocket.sendto(messageDom.encode('utf-8'), DNS_REP_ADDR)
    print("Domain sent to DNS server")

    Clientsocket.sendto(messageAddr.encode('utf-8'), DNS_REP_ADDR)
    print("Address sent to DNS server")

    Clientsocket.close()
    print("Socket Closed")

def handle_client(index):

    while True:
        msg = server.recvMessage(index)
        if msg == "checkFiles":
            print("\nFiles in your folder:")
            files = os.listdir(FOLDER)
            dim = str(len(files))
            server.sendMessage(dim,index)

            for i in files:
                server.sendMessage(i,index)
                print(i)
            print("\n")

        elif msg == "download":
            fileName = server.recvMessage(index)
            if (os.path.isfile(FOLDER + fileName)): #verifica se o arquivo que se deseja baixar está contido no servidor
                server.sendMessage("exist",index)
                server.sendMessage((str(os.path.getsize(FOLDER + fileName))), index)
                arq = open(FOLDER + fileName, 'rb')
            
                for line in arq:
                    server.connectedSockets[index].send(line)

                arq.close()

                print ("File successfully downloaded\n")
            else:
                server.sendMessage("notExist",index)
                print ("File not successfully downloaded\n")
def main():

    sendToDNS()
    while True:
        index = server.acceptConnection()
        num = _thread.start_new_thread(handle_client, (index,))
                    
    return  

if __name__ == "__main__":
    main()


