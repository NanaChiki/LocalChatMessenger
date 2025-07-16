import os
import socket
from faker import Faker
from datetime import datetime

def get_timestamp():
    """
    Returns current timestamp in YYYY-MM-DD HH:MM:SS format.

    Returns:
        str: Formatted timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def cleanup_socket_file(filepath):
    """
    Cleans up a socket file by removing it if it exists.

    Args:
        filepath (str): Path to the socket file to be cleaned up
    """
    try:
        os.unlink(filepath)
    except FileNotFoundError:
        pass

def main():
    """
    Main function to start the UDP server.

    This function initializes the server, binds it to a socket file, and waits for messages.
    It processes incoming messages and generates fake responses using the Faker library.
    """
    fake = Faker()
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    server_address = '/tmp/udp_socket_file'

    try:
        cleanup_socket_file(server_address)
        sock.bind(server_address)
        print('Starting up on {}'.format(server_address))

        while True:
            print('\nWaiting to receive message...😊')

            # 4096 is the max byte size that can be received at a time
            data, address = sock.recvfrom(4096)
            timestamp = get_timestamp()

            # Send the data back to the sender
            fake_data = None
            if data:
                if 'name' in data.decode(): 
                    fake_data = fake.name()
                elif 'address' in data.decode():
                    fake_data = fake.address()
                elif 'email' in data.decode():
                    fake_data = fake.email()
                elif 'text' in data.decode():
                    fake_data = fake.text()
                else:
                    # Data is defaulted to a random fake sentence
                    fake_data = fake.sentence()
                
                response = sock.sendto(fake_data.encode(), address)
                print(f'📥 \033[94m[{timestamp}] Received: \033[0m {len(data)} bytes from {address}')
                print(f'📩 \033[94m[{timestamp}] Message: \033[0m {data.decode()}')
                print(f'📤 \033[92m[{timestamp}] Sent response: \033[0m {response} bytes to {address}')
                print(f'📩 \033[92m[{timestamp}] Response: \033[0m {fake_data}')
    except KeyboardInterrupt:
        print('\n👋 Server shutting down gracefully')
    except Exception as e:
        print(f'❌ Fatal error: {e}')

    finally:
        sock.close()
        cleanup_socket_file(server_address)
        print('🧹 Cleanup completed')

if __name__ == "__main__":
    main()