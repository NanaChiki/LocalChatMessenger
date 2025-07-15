import socket
import sys
import os

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

server_address = '/tmp/udp_socket_file'

address = '/tmp/udp_client_socket_file'

message = input("Enter your message to send to the server: ")

try:
    os.unlink(address)
except FileNotFoundError:
    pass

# Bind the client address to the socket
try:
    sock.bind(address)
except socket.error as e:
    print('Socket connection failed: {}'.format(e))
    sys.exit(1)

# Send a message to the server
# try:
# Create a loop that allows multiple messages without restarting
loop = True
while loop:
    print('Sending {!r}'.format(message))
    # message = message.encode()
    sent = sock.sendto(message.encode(), server_address)

    # Receive 4096 bytes data at the maximum
    print('Waiting to receive')

    data, server = sock.recvfrom(4096)

    # Display the received data from the server
    # data_str = data.decode('utf-8')
    print('Received message in binary: {!r}'.format(data))
    # print('Received message in string: {!s}'.format(data))
    # print('Received message in string: {!a}'.format(data))
    print('The message is sent from: {!r}'.format(server))

    question = input("Would you like to send another message? Y/N ")
    while True:
        if question == "Y":
            message = input("Enter your message to send to the server: ")
            break
        elif question =="N":
            loop = False
            break
        question = input("Would you like to send another message? Y/N ")

# finally:
#     print('Closing socket')
#     sock.close()
