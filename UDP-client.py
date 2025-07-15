import socket
import sys
import os
from datetime import datetime


# Function to get formatted timestamp
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

server_address = '/tmp/udp_socket_file'
address = '/tmp/udp_client_socket_file'


try:
    # Delete a previous address and bind the new one to the socket
    os.unlink(address)
    sock.bind(address)

    # Send a message to the server
    # Create a loop that allows multiple messages without restarting
    
    while True:
        message = input("Enter your message (or 'quit' to exit): ")
        if message.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break # This exists the while loop
        
        timestamp = get_timestamp()
        print(f'📤 [{timestamp}] Sending to Server: {message}')
        sent = sock.sendto(message.encode(), server_address)

        # Receive 4096 bytes data at the maximum
        print('Waiting to receive...')

        data, server = sock.recvfrom(4096)

        # Display the received data from the server
        timestamp = get_timestamp()
        print(f'📩 [{timestamp}] Received from Server: {data}')

except Exception as e:
    print('Error: {}'.format(e))
    sys.exit(1)

finally:
    print('Closing socket')
    sock.close()
