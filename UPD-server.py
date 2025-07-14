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
  print('The message received is {}'.format(data.decode('utf-8')))

  # Send the data back to the sender
  if data:
    # sent = sock.sendto(data, address)
    fake_name = fake.name()
    fake_address = fake.address()
    response = sock.sendto(fake_name.encode(), address)
    print('Sent {} bytes back to {}'.format(response, address))

  
