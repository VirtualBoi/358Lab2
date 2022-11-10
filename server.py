
from socket import *
import random

domain = ""
TTL = 0
IP_address = 0
record = 0

# response information
# DNS header
ID = random.randint(0, 65535)
QR = ""  # query = 0, response = 1
OPCODE, TC, RD, RA, RCODE, NSCOUNT, ARCOUNT = 0, 0, 0, 0, 0, 0, 0
AA, QDCOUNT = 1, 1
Z = "000"
FLAGS = ""
ANCOUNT = ""  # an unsigned 16-bit integer specifying the number of resource records in the answer section.


# query
QNAME = ""
QTYPE = "A"
QCLASS = "IN"  # Set QCLASS field as IN (00 01) (hex value) for the Internet.

# answer
NAME = "c0 0c"
TYPE = "41"  # type A in hex
CLASS = "49 4e"  # only deal with IN class
# TTL = 0
RDLENGTH = ""  # an unsigned 16 bit integer that specifies the length in octets of the RDATA field
RDATA = ""  # a variable length string of octets that describes the resource. The format of this information
            # varies according to the TYPE and CLASS of the resource record


def domain_data(domain_name):
    global TTL
    global IP_address
    global domain

    domain = domain_name
    if domain == "google.com":
        TTL = 260
        IP_address = ("192.165.1.1", "192.165.1.10")
    elif domain == "youtube.com":
        TTL = 160
        IP_address = "192.165.1.2"
    elif domain == "uwaterloo.ca":
        TTL = 160
        IP_address = "192.165.1.3"
    elif domain == "wikipedia.org":
        TTL = 160
        IP_address = "192.165.1.4"
    elif domain == "amazon.ca":
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
    print("\033[4mRequest:\033[0m")
    # print(message + "\n")
    if domain_data(message):
        modifiedMessage = "Unknown domain name"
    elif message == "google.com":
        modifiedMessage = ("{}: type {}, class {}, TTL {}, addr ({}) {}\n{}: type {}, class {}, TTL {}, addr ({}) {}"
                           .format(domain, QTYPE, QCLASS, TTL, record, IP_address[0], domain, QTYPE, QCLASS, TTL, record, IP_address[1]))
    else:
        modifiedMessage = ("{}: type {}, class {}, TTL {}, addr ({}) {}".format(domain, QTYPE, QCLASS, TTL, record, IP_address))
    print("\033[4mResponse:\033[0m")
    # print(modifiedMessage + "\n")
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)

