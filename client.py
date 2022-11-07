
from socket import *

serverIP = "127.0.0.1"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = raw_input("Enter Domain Name: ")

clientSocket.sendto(message.encode(), (serverIP, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print (modifiedMessage.decode())
clientSocket.close()
