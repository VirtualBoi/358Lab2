# http://127.0.0.1:10000/HelloWorld.html

from socket import *
import re
import datetime
import time
import os

path = "HelloWorld.html"
serverIP = "127.0.0.1"
serverPort = 10000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)

#list all files that are in directory
files = []
for (dir_path, dir_names, file_names) in os.walk(os.getcwd()):
    files.extend(file_names)
#if ("HelloWorld.html" in files):

#404 not found html
not_found = "<html>\r\n<body>\r\n<center>\r\n<h3>Error 404: File not found</h3>\r\n</center>\r\n</body>\r\n</html>"
response = ""

# header min 6 lines
connection = "Connection: close"
date = ""
server = "Server: J.Ko & E.Gilbert " + serverIP
timestamp_mod = ""
content_len = ""
content_type = ""

def main():
    
    #algorithm
    while True:
        #Update Header variables
        date = ""
        timestamp_mod = ""
        content_len = ""
        content_type = ""
        
        #recieve from Client
        connectionSocket, addr = serverSocket.accept()
        request = connectionSocket.recv(2048).decode()

        #update header variables
        date = "Date: "+ datetime.datetime.today().strftime('%a, %d %b %Y %I:%M:%S %Z') + " GMT"

        #parse request message
        request_type_reg = re.search("([^ ]+)", request)
        file_reg = re.search("\s+([^\s]+)", request)
        request_type = request_type_reg.group()
        file_name = file_reg.group()[2:]

        #default header variables
        html_text = ""
        response = "HTTP/1.1 400 Bad Request \r\n" #default respond with 404 not found
        header = ""

        #search for requested file
        if (file_name in files):
            html_text = open(file_name, "r").read()

            #update header variables
            ti_m = os.path.getmtime(file_name)
            m_ti = time.ctime(ti_m)

            timestamp_mod = "Last-Modified: " + datetime.datetime.fromtimestamp(ti_m).strftime('%a, %d %b %Y %I:%M:%S %Z') + "GMT" #get last modified timestamp
            content_len = "Content-Length: " + str(os.stat(file_name).st_size)
            content_type = "Content-Type: text/html; charset=UTF-8"

            header = connection + "\n" + date + "\n" + server + "\n" + timestamp_mod + "\n" + content_len + "\n" + content_type + "\n"

            #setting up response message given file name exists
            if (request_type == "GET"):
                response = "HTTP/1.1 200 OK \r\n"
                final_response = response+header+'\n'+html_text

            elif (request_type == "HEAD"):
                response = "HTTP/1.1 200 OK \r\n"
                final_response = response+header+'\n'

            else:
                print ("Please request get OR head")

        else:
            response = "HTTP/1.1 404 Not Found \r\n"
            header = connection + "\n" + date + "\n" + server + "\n" + timestamp_mod + "\n" + content_len + "\n" + content_type + "\n"
            html_text = not_found   
            final_response = response+header+'\n'+html_text


        #Send full HTTP response
        connectionSocket.sendall((final_response).encode())

        connectionSocket.close()
 
if __name__ == "__main__":
    main()
