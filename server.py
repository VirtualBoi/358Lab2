
from socket import *

serverIP = "127.0.0.1"
serverPort = 12000
domain = ""

# answer
NAME = "c0 0c"
TYPE = "00 01"  # type A in hex
CLASS = "00 01"  # only deal with IN class
TTL = ""
RDLENGTH = ""
RDATA = ""
RDATA2 = ""


# updating the flags for a response instead of a query (swapping first bit and changing back to hex)
def update_flags(in_flags):
    hex_temp = in_flags.replace(" ", "")
    bin_temp = list((bin(int(hex_temp, 16)).replace("b", "")).zfill(16))
    bin_temp[0] = '1'
    bin_temp = "".join(bin_temp)
    split_input = (hex(int(bin_temp, 2)).lstrip("0x"))
    half1 = split_input[:len(split_input) // 2].zfill(2)
    half2 = split_input[len(split_input) // 2:].zfill(2)
    return half1 + " " + half2


# lookup table of all domains and relevant information
def domain_data(domain_name):
    global TTL
    global RDATA
    global RDATA2
    global RDLENGTH
    global domain

    domain = domain_name
    if domain == "67 6f 6f 67 6c 65 2e 63 6f 6d":  # google.com
        TTL = "01 04"  # 260
        RDATA = "c0 a5 01 01"  # 192.165.1.1
        RDATA2 = "c0 a5 01 0a"  # 192.165.1.10
        RDLENGTH = "00 04"
    elif domain == "79 6f 75 74 75 62 65 2e 63 6f 6d":  # youtube.com
        TTL = "00 A0"  # 160
        RDATA = "c0 a5 01 02"  # 192.165.1.2
        RDLENGTH = "00 04"
    elif domain == "75 77 61 74 65 72 6c 6f 6f 2e 63 61":  # uwaterloo.ca
        TTL = "00 A0"  # 160
        RDATA = "c0 a5 01 03"  # 192.165.1.3
        RDLENGTH = "00 04"
    elif domain == "77 69 6b 69 70 65 64 69 61 2e 6f 72 67":  # wikipedia.org
        TTL = "00 A0"  # 160
        RDATA = "c0 a5 01 04"  # 192.165.1.4
        RDLENGTH = "00 04"
    elif domain == "61 6d 61 7a 6f 6e 2e 63 61":  # amazon.ca
        TTL = "00 A0"  # 160
        RDATA = "c0 a5 01 05"  # 192.165.1.5
        RDLENGTH = "00 04"
    else:
        return 1
    return 0


def main():
    global domain

    # starting server socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind((serverIP, serverPort))

    while True:
        # receiving message from client
        message, clientAddress = serverSocket.recvfrom(2048)
        message = message.decode()
        if message == "end":
            exit(0)
            serverSocket.close()

        query = message[36:]
        domain = query[0:-12]

        # printing coloured request
        print("\033[4mRequest:\033[0m")
        print("\033[36m" + message[0:5] + "\033[30m" + message[5:11] + "\033[33m" + message[11:17] + "\033[31m" +
              message[17:23] + "\033[32m" + message[23:29] + "\033[34m" + message[29:35], end='')
        print("\033[35m" + message[35:len(query) + 25] + "\033[36m" + message[-11:-5] + "\033[30m" + message[-5:] + "\033[0m\n")

        print("\033[4mResponse:\033[0m")
        answer2 = ""

        # if unknown domain send that as response
        if domain_data(domain):
            modifiedMessage = "55 6E 6B 6E 6F 77 6E 20 64 6F 6D 61 69 6E 20 6E 61 6D 65"  # "Unknown domain name" in hex
        else:
            # breaking message into header and question components
            hex_ID = message[0:5]
            hex_FLAGS = message[6:11]
            hex_FLAGS = update_flags(hex_FLAGS)
            QDCOUNT = message[12:17]
            ANCOUNT = message[18:23]
            NSCOUNT = message[24:29]
            ARCOUNT = message[30:35]

            # combining parts of response 
            DNS_header = hex_ID + " " + hex_FLAGS + " " + QDCOUNT + " " + ANCOUNT + " " + NSCOUNT + " " + ARCOUNT
            answer = NAME + " " + TYPE + " " + CLASS + " " + TTL + " " + RDLENGTH + " " + RDATA
            if domain == "67 6f 6f 67 6c 65 2e 63 6f 6d":
                answer2 = NAME + " " + TYPE + " " + CLASS + " " + TTL + " " + RDLENGTH + " " + RDATA2
            modifiedMessage = DNS_header + " " + query + " " + answer + " " + answer2

            # prints colour coded header
            print("\033[36m" + modifiedMessage[0:5] + "\033[30m" + modifiedMessage[5:11] + "\033[33m" +
                modifiedMessage[11:17] + "\033[31m" + modifiedMessage[17:23] + "\033[32m" + modifiedMessage[23:29] +
                "\033[34m" + modifiedMessage[29:35] + "\033[35m", end='')

            # prints colour coded query
            print(modifiedMessage[35:len(query) + 25] + "\033[36m" + modifiedMessage[len(query) + 25:len(query) + 30] +
                "\033[30m" + modifiedMessage[len(query) + 30:len(query) + 36], end='')

            # prints colour coded response (adds extra answer for domains with multiple IPs)
            print(" \033[36m" + NAME + "\033[33m " + TYPE + "\033[35m " + CLASS + "\033[31m " + TTL + "\033[34m " + RDLENGTH
                + "\033[32m " + RDATA + "\033[0m", end='')
            if answer2 != "":
                print(" \033[36m" + NAME + "\033[33m " + TYPE + "\033[35m " + CLASS + "\033[31m " + TTL + "\033[34m " +
                    RDLENGTH + "\033[32m " + RDATA2 + "\033[0m", end='')

        print("\n")
        
        # sends response back to client
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)


if __name__ == "__main__":
    main()
