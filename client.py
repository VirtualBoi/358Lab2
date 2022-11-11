from socket import *
import random
import re

serverIP = "127.0.0.1"
serverPort = 12000

# fucntion to split hex values for proper display
def split_hex(in_hex):
    split_input = (hex(int(in_hex, 2)).lstrip("0x"))
    half1 = split_input[:len(split_input) // 2].zfill(2)
    half2 = split_input[len(split_input) // 2:].zfill(2)
    return half1 + " " + half2


# DNS header

# flags (bits) QR - Opcode - AA - TC - RD - RA - Z - RCODE
QR = "0"  # 0 for query, 1 for response
OPCODE = "0000"
TC, RD, RA, = "0", "0", "0"
AA = "1"
Z = "000"
RCODE = "0000"
QDCOUNT = "00 01"
ANCOUNT = "00 00" 
NSCOUNT, ARCOUNT = "00 00", "00 00"
bin_FLAGS = QR + OPCODE + AA + TC + RD + RA + Z + RCODE
hex_FLAGS = split_hex(bin_FLAGS)

# query
QTYPE = "00 01"  # is type 'A"
QCLASS = "00 01"  # Set QCLASS field as IN (00 01) (hex value) for the Internet.


# combining output message for output
def output(domain_response, type_response, class_response, TTL_response, len_response, address_response):
    outputMessage = domain_response + ": type " + type_response + ", class " + class_response + ", TTL " + \
                    str(TTL_response) + ", addr (" + str(len_response) + ") " + address_response
    print(outputMessage)


def main():
    while True:
        # start client socket
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        # read input from user
        print("\033[4mInput from the user:\033[0m")
        message = input("Enter Domain Name: ")
        QNAME = ""

        # end session
        if message == "end":
            print("Session ended")
            message = "end"
            clientSocket.sendto(message.encode(), (serverIP, serverPort))
            clientSocket.close()
            exit(0)
        
        # creating random ID
        ID = random.randint(0, 65535)
        bin_ID = '{0:08b}'.format(ID)
        hex_ID = split_hex(bin_ID)

        for i in message:
            QNAME += hex(ord(i)).lstrip("0x") + " "

        # combining message elements to be sent
        DNS_header = hex_ID + " " + hex_FLAGS + " " + QDCOUNT + " " + ANCOUNT + " " + NSCOUNT + " " + ARCOUNT
        query = QNAME + QTYPE + " " + QCLASS
        message = DNS_header + " " + query

        # sending message to server
        clientSocket.sendto(message.encode(), (serverIP, serverPort))

        # receiving message from server
        outputMessage, serverAddress = clientSocket.recvfrom(2048)
        outputMessage = outputMessage.decode()

        print("\n\033[4mOutput:\033[0m")

        # if unknown domain
        if outputMessage == "55 6E 6B 6E 6F 77 6E 20 64 6F 6D 61 69 6E 20 6E 61 6D 65":
            print("Unknown domain name")
        else:
            id_bytes = ["", "", "", ""]

            # splitting response into known sections of query and domain
            query_response = outputMessage[36:len(query) + 36]
            domain_response = bytes.fromhex(query_response[0:-12]).decode('utf-8')

            # searches response for c0 0c identifier
            num_of_ids = len(re.findall("c0 0c", outputMessage))
            res = re.search("(c0 0c)", outputMessage)

            # read response and translate hex to text (takes multiple IP addresses)
            for i in range(num_of_ids):
                index = res.end() + 1 + i*42

                # confirms correct type and class
                if outputMessage[index:index + 5] == "00 01":
                    type_response = "A"
                else:
                    type_response = "N/A"
                if outputMessage[index + 6:index + 11] == "00 01":
                    class_response = "IN"
                else:
                    class_response = "N/A"

                # reads in TTL and RDLENGTH
                TTL_response = int(((outputMessage[index + 12: index + 17]).replace(" ", "")), 16)
                len_response = int(((outputMessage[index + 18: index + 23]).replace(" ", "")), 16)

                # read IP address and put it into proper form
                for x in range(4):
                    id_bytes[x] = int((outputMessage[index + 24 + x*3: index + 26 + x*3]), 16)
                address_response = str(id_bytes[0]) + "." + str(id_bytes[1]) + "." + str(id_bytes[2]) + "." + str(id_bytes[3])
                output(domain_response, type_response, class_response, TTL_response, len_response, address_response)

        print("")

        # closing socket
        clientSocket.close()


if __name__ == "__main__":
    main()
