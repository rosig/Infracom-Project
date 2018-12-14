from socket import socket, AF_INET, SOCK_DGRAM, timeout
from common import calcChecksum

class Socket:
    send_socket = socket(AF_INET,SOCK_DGRAM)
    recv_socket = socket(AF_INET,SOCK_DGRAM)
    seq = 0
    expected_seq = 0

    def bind(self, recv_addr, recv_port): # Bind the receiver socket
        self.recv_port = recv_port
        self.recv_socket.bind((recv_addr, recv_port))
    
    def send(self, data, server_addr, server_port): # Send data to server
        dest = (server_addr, server_port)
        pack = (
            str(self.recv_port) +
            calcChecksum(data) +
            str(self.seq) +
            data
        ).encode('utf-8')

        ack_received = False
        while not ack_received:
            self.send_socket.sendto(pack, dest)
            try:
                message, address = self.recv_socket.recvfrom(4096)
            except timeout:
                pass
            else:
                checksum = message.decode('utf-8')[:2]
                seq = int(message.decode('utf-8')[5])
                if calcChecksum(message.decode('utf-8')[2:]) == checksum and seq == self.seq:
                    ack_received = True
        self.seq = 1-self.seq
    
    def receive(self): # Receive data from the client 
        message, address = self.recv_socket.recvfrom(4096)
        
        cli_addr = 'localhost'
        cli_port = int(message.decode('utf-8')[:5])
        checksum = message.decode('utf-8')[5:7]
        seq = int(message.decode('utf-8')[7])
        content = message.decode('utf-8')[8:]

        dest = (cli_addr, cli_port)

        resp = 'ACK' + str(seq)
        pack = (
            calcChecksum(resp) +
            resp
        ).encode('utf-8')

        inv_resp = 'ACK' + str(1-self.expected_seq)
        inv_pack = (
            calcChecksum(inv_resp) +
            inv_resp
        ).encode('utf-8')

        if calcChecksum(content) == checksum:
            self.send_socket.sendto(pack, dest)
            if seq == self.expected_seq:
                self.expected_seq = 1-self.expected_seq
                return (cli_addr, cli_port, content)
            else:
                self.send_socket.sendto(inv_pack, dest)
                return -1
        return -1