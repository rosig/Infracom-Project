from lib.constants import *
from socket import *

class TCPServerSocket:
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.connectedSockets = []
        self.socket.bind(('', CLI_REP_PORT))
        self.socket.listen(1)

    def acceptConnection(self):
        connSocket = self.socket.accept()[0]
        self.connectedSockets.append(connSocket)
        print("Connected")
        return self.connectedSockets.index(connSocket)

    def recvMessage(self, ind):
        sock = self.connectedSockets[ind]
        msg = sock.recv(BUFFER_SIZE)
        return msg.decode('utf-8')

    def sendMessage(self, msg, ind):
        self.connectedSockets[ind].send(msg.encode('utf-8'))

    def closeConnection(self, ind):
        self.connectedSockets[ind].close()

    def close(self):
        self.socket.close()
