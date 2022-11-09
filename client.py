
from socket import *

serverIP = "127.0.0.1"
serverPort = 12000

while True:
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    print("\033[4mInput from the user:\033[0m")
    message = raw_input("Enter Domain Name: ")

    print("\n\033[4mOutput:\033[0m")
    if message == "end":
        print("Session ended")
        clientSocket.close()
        exit(0)

    clientSocket.sendto(message.encode(), (serverIP, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode() + "\n")
    clientSocket.close()
