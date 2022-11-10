
from socket import *

domain = ""

# answer
NAME = "c0 0c"
TYPE = "00 01"  # type A in hex
CLASS = "00 01"  # only deal with IN class
TTL = "00 00 00 00"
RDLENGTH = ""
RDATA = ""


def update_flags(in_flags):
    hex_temp = in_flags.replace(" ", "")
    bin_temp = list((bin(int(hex_temp, 16)).replace("b", "")).zfill(16))
    bin_temp[0] = '1'
    bin_temp = "".join(bin_temp)
    split_input = (hex(int(bin_temp, 2)).lstrip("0x"))
    half1 = split_input[:len(split_input) // 2].zfill(2)
    half2 = split_input[len(split_input) // 2:].zfill(2)
    return half1 + " " + half2


def domain_data(domain_name):
    global TTL
    global RDATA
    global domain

    domain = domain_name
    if domain == "67 6f 6f 67 6c 65 2e 63 6f 6d":  # google.com
        TTL = "01 04"  # 260
        RDATA = ("01 25 38 7F" + " " + "0B 74 34 F6") # 192.165.1.1 and 192.165.1.10
        RLENGTH = ("00 08")
    elif domain == "79 6f 75 74 75 62 65 2e 63 6f 6d":  # youtube.com
        TTL = "00 A0"  # 160
        RDATA = "01 25 38 80" # 192.165.1.2
        RLENGTH = "00 04"
    elif domain == "75 77 61 74 65 72 6c 6f 6f 2e 63 61":  # uwaterloo.ca
        TTL = "00 A0"  # 160
        RDATA = "01 25 38 81" # 192.165.1.3
        RLENGTH = "00 04"
    elif domain == "77 69 6b 69 70 65 64 69 61 2e 6f 72 67":  # wikipedia.org
        TTL = "00 A0"  # 160
        RDATA = "01 25 38 82" # 192.165.1.4
        RLENGTH = "00 04"
    elif domain == "61 6d 61 7a 6f 6e 2e 63 61":  # amazon.ca
        TTL = "00 A0"  # 160
        RDATA = "01 25 38 83" # 192.165.1.5
        RLENGTH = "00 04"
    else:
        return 1
    return 0


def main():
    serverIP = "127.0.0.1"
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind((serverIP, serverPort))
    print ("The server is ready to receive")

    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        message = message.decode()
        print("\033[4mRequest:\033[0m")
        print(message + "\n")

        # breaking message into header and question components
        hex_ID = message[0:5]
        hex_FLAGS = message[6:11]
        hex_FLAGS = update_flags(hex_FLAGS)
        QDCOUNT = message[12:17]
        ANCOUNT = message[18:23]
        NSCOUNT = message[24:29]
        ARCOUNT = message[30:35]
        DNS_header = hex_ID + " " + hex_FLAGS + " " + QDCOUNT + " " + ANCOUNT + " " + NSCOUNT + " " + ARCOUNT
        query = message[36:]
        domain = query[0:-12]
        answer = NAME + " " + TYPE + " " + CLASS + " " + TTL + " " + RDLENGTH + " " + RDATA
        modifiedMessage = DNS_header + " " + query + " " + answer

        if domain_data(domain):
            modifiedMessage = "55 6E 6B 6E 6F 77 6E 20 64 6F 6D 61 69 6E 20 6E 61 6D 65"  # "Unknown domain name" in hex
        else:
            print("\033[4mResponse:\033[0m")
            print(modifiedMessage + "\n")
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)

        
        """
        elif message == "google.com":
            modifiedMessage = ("{}: type {}, class {}, TTL {}, addr ({}) {}\n{}: type {}, class {}, TTL {}, addr ({}) {}"
                               .format(domain, QTYPE, QCLASS, TTL, record, IP_address[0], domain, QTYPE, QCLASS, TTL, record, IP_address[1]))
        else:
            modifiedMessage = ("{}: type {}, class {}, TTL {}, addr ({}) {}".format(domain, QTYPE, QCLASS, TTL, record, IP_address))
        """
        """
        
        print("\033[36m" + modifiedMessage[0:5] + "\033[30m" + modifiedMessage[5:11] + "\033[33m" +
              modifiedMessage[11:17] + "\033[31m" + modifiedMessage[17:23] + "\033[32m" + modifiedMessage[23:29] +
              "\033[34m" + modifiedMessage[29:35] + "\033[35m" + modifiedMessage[35:len(query) + 25] + "\033[36m" +
              modifiedMessage[-10:-5] + "\033[30m" + modifiedMessage[-7:])
        """
        


if __name__ == "__main__":
    main()
