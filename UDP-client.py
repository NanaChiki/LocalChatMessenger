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
try:
    print('Sending {!r}'.format(message))
    message = message.encode()
    sent = sock.sendto(message, server_address)

    # Receive 4096 bytes data at the maximum
    print('Waiting to receive')
    data, server = sock.recvfrom(4096)

    # Display the received data from the server
    data_str = data.decode('utf-8')
    print('Received message in binary: {}'.format(data))
    print('Received message in string: {!r}'.format(data_str))
    print('The message is sent from: {}'.format(server))

finally:
    print('Closing socket')
    sock.close()
