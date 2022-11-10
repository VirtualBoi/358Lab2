
from socket import *
import random

serverIP = "127.0.0.1"
serverPort = 12000


def split_hex(in_hex):
    split_input = (hex(int(in_hex, 2)).lstrip("0x"))
    half1 = split_input[:len(split_input) / 2].zfill(2)
    half2 = split_input[len(split_input) / 2:].zfill(2)
    return half1 + " " + half2


# DNS header
# ID generator
ID = random.randint(0, 65535)
bin_ID = '{0:08b}'.format(ID)
hex_ID = split_hex(bin_ID)

# flags (bits) QR - Opcode - AA - TC - RD - RA - Z - RCODE
QR = "0"  # 0 for query, 1 for response
OPCODE = "0000"
TC, RD, RA,  = "0", "0", "0"
AA = "1"
Z = "000"
RCODE = "0000"
QDCOUNT = "00 01"
ANCOUNT = "00 00"  # an unsigned 16-bit integer specifying the number of resource records in the answer section.
NSCOUNT, ARCOUNT = "00 00", "00 00"
bin_FLAGS = QR + OPCODE + AA + TC + RD + RA + Z + RCODE
hex_FLAGS = split_hex(bin_FLAGS)

# query
QTYPE = "00 01"  # is type 'A"
QCLASS = "00 01"  # Set QCLASS field as IN (00 01) (hex value) for the Internet.


def main():
    while True:
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        print("\033[4mInput from the user:\033[0m")
        message = raw_input("Enter Domain Name: ")
        QNAME = ""

        print("\n\033[4mOutput:\033[0m")
        if message == "end":
            print("Session ended")
            clientSocket.close()
            exit(0)

        for i in message:
            QNAME += hex(ord(i)).lstrip("0x") + " "

        DNS_header = hex_ID + " " + hex_FLAGS + " " + QDCOUNT + " " + ANCOUNT + " " + NSCOUNT + " " + ARCOUNT
        query = QNAME + QTYPE + " " + QCLASS
        # print(DNS_header)
        # print(QNAME)
        message = DNS_header + " " + query

        clientSocket.sendto(message.encode(), (serverIP, serverPort))
        outputMessage, serverAddress = clientSocket.recvfrom(2048)
        header_response = outputMessage[0:35].replace(" ", "")
        query_response = outputMessage[36:].replace(" ", "")
        if len(query_response) % 2 != 0:
            query_response = query_response.zfill(len(query_response)+1)
        print(query_response)
        print(query_response.decode("hex"))

        print(outputMessage.decode() + "\n")
        clientSocket.close()


if __name__ == "__main__":
    main()
