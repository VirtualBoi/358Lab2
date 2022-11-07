
from socket import *

domain = ""
domainType = ""
domainClass = ""
TTL = 0
IP_address = 0
record = 0


def domain_data(domain_name):
    global domainType
    global domainClass
    global TTL
    global IP_address
    global domain

    domain = domain_name
    if domain == "google.com":
        domainType = "IN"
        domainClass = 'A'
        TTL = 260
        IP_address = ("192.165.1.1", "192.165.1.10")
    elif domain == "youtube.com":
        domainType = "IN"
        domainClass = 'A'
        TTL = 160
        IP_address = "192.165.1.2"
    elif domain == "uwaterloo.ca":
        domainType = "IN"
        domainClass = 'A'
        TTL = 160
        IP_address = "192.165.1.3"
    elif domain == "wikipedia.org":
        domainType = "IN"
        domainClass = 'A'
        TTL = 160
        IP_address = "192.165.1.4"
    elif domain == "amazon.ca":
        domainType = "IN"
        domainClass = 'A'
        TTL = 160
        IP_address = "192.165.1.5"
    else:
        return 1
    return 0


serverIP = "127.0.0.1"
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))
print ("The server is ready to receive")

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print(message)
    if domain_data(message):
        modifiedMessage = "Unknown domain name"
    elif message == "google.com":
        modifiedMessage = ("{}: type {}, class {}, TTL {}, addr ({}) {}\n{}: type {}, class {}, TTL {}, addr ({}) {}"
                           .format(domain, domainType, domainClass, TTL, record, IP_address[0], domain, domainType, domainClass, TTL, record, IP_address[1]))
    else:
        modifiedMessage = ("{}: type {}, class {}, TTL {}, addr ({}) {}".format(domain, domainType, domainClass, TTL, record, IP_address))
    # modifiedMessage = message.decode().upper()
    # print(modifiedMessage)
    # print(clientAddress)
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)

