# echo -n 0x03 | nc 127.0.0.1 1234

# how to send GET vs HEAD request

from socket import *
import re
import time
import os


path = "HelloWorld.html"
serverIP = "127.0.0.1"
serverPort = 10000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)

print ("The server is ready to receive")

# header min 6 lines
connection = serverPort
time_sent = ""
server = serverIP
time_mod = os.path.getmtime(path)
timestamp_mod = time.ctime(time_mod)
content_len = ""
content_type = ""

# algorithm
while True:

    connectionSocket, addr = serverSocket.accept()
    request = connectionSocket.recv(2048).decode()
    # print (request)
    request_type = re.search("([^ ]+)", request)
    print (request_type.group())

    # connectionSocket.send("bruh")
    connectionSocket.close()
