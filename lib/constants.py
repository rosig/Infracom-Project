#Constants
import platform
import os

SERVER_PORT = 12015
CLI_REP_PORT = 14740
DNS__REP_PORT = 14750
DNS_CLI_PORT = 14810
BUFFER_SIZE = 2048
DOMAIN_SERVER = "www.MARE.com.br"

DNS_REP_ADDR = ('localhost', DNS__REP_PORT)
DNS_CLI_ADDR = ('localhost', DNS_CLI_PORT)

#altere somente a string da esquerda
FOLDER = os.path.join(os.getcwd(), "server")
FOLDER_CLI = os.path.join(os.getcwd(), "client")
#FOLDER = "C:\\Users\\ROSINALDO\\Desktop\\Infracom-Project" + "\\SERVIDOR\\"
#FOLDER_CLI = "C:\\Users\\ROSINALDO\\Desktop\\Infracom-Project" + "\\CLIENTE\\"
