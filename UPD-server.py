import os
import socket
from faker import Faker

fake = Faker()

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

server_address = '/tmp/udp_socket_file'

try:
    # Delete a previous socket file if there is one
    os.unlink(server_address)
except FileNotFoundError:
    pass

print('Starting up on {}'.format(server_address))

sock.bind(server_address)

while True:
    print('\nWaiting to receive message')
    # 4096 is the max byte size that can be received at a time
    data, address = sock.recvfrom(4096)
    # The byte size of the data received and the address sent data from
    print('Received {} bytes from {}'.format(len(data), address))
    print('The message received is {}'.format(data))

    # Send the data back to the sender
    if data:
        if 'name' in data.decode():
            data = fake.name()
        elif 'address' in data.decode():
            data = fake.address()
        elif 'email' in data.decode():
            data = fake.email()
        elif 'text' in data.decode():
            data = fake.text()
        else:
            # Data is defaulted to a random fake sentence
            data = fake.sentence()

        response = sock.sendto(data.encode(), address)
        print('Sent {} bytes back to {}'.format(response, address))

