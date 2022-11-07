
from socket import *

serverIP = "127.0.0.1"
serverPort = 12000

while True:
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = raw_input("Enter Domain Name: ")
    if message == "end":
        print("Session ended")
        clientSocket.close()
        exit(0)

    clientSocket.sendto(message.encode(), (serverIP, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print (modifiedMessage.decode())
    clientSocket.close()
