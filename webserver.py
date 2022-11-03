#bruh
#echo -n 0x03 | nc 127.0.0.1 1234

#how to send GET vs HEAD request

from socket import *
serverIP = "127.0.0.1"
serverPort = 10000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)

print ("The server is ready to receive")

#algorithm
while True:

    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(2048).decode()

    if head:
        connectionSocket.send("yep - is there ;p")
    else:
        connectionSocket.send("1010100101010101010100101000101111010101010")

    connectionSocket.close()