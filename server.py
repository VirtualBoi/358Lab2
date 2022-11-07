
from socket import *


serverIP = "127.0.0.1"
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))
print ("The server is ready to receive")

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print(message)
    modifiedMessage = message.decode().upper()
    print(modifiedMessage)
    print(clientAddress)
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
