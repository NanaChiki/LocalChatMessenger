import socket
import sys
import os
from datetime import datetime


# Function to get formatted timestamp
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def cleanup_socket_file(filepath):
    # Clean up client socket file
    try:
        os.unlink(filepath)
    except FileNotFoundError:
        pass


def main():
    # Socket setup
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    server_address = '/tmp/udp_socket_file'
    client_address = '/tmp/udp_client_socket_file'

    try:
        # Cleanup any existing client socket file
        cleanup_socket_file(client_address)

        # Bind client socket file to the socket
        sock.bind(client_address)
        sock.settimeout(5.0) # Set timeout

        print("🚀 UDP Client started! Type 'quit' to exit.")

        # Create a loop that allows multiple messages without restarting
        while True:
            message = input("Enter your message (or 'quit' to exit): ")
            if message.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break # This exists the while loop
            
            timestamp = get_timestamp()
            sock.sendto(message.encode(), server_address)
            print(f'📤 [{timestamp}] Sending to Server: {message}')

            # Receive 4096 bytes data at the maximum
            print('Waiting to receive...')
            
            data, server = sock.recvfrom(4096)
            timestamp = get_timestamp()
            # Display the received data from the server
            print('📩 [{a}] Received: {!r}, Server address: {}'.format(timestamp, data, server))
    
    except KeyboardInterrupt:
        print("\n👋 Client interrupted by user")

    except socket.timeout:
        print("⚠️ Server did not respond within 5 seconds. Server might be down.")
        print("   Continue sending messages or type 'quit' to exit.")

    except ConnectionRefusedError:
        print("❌ Cloud not connect to server. Is the server running?")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Cleanup
        sock.close()
        cleanup_socket_file(client_address)
        print('🧹 Cleanup completed')

if __name__ == "__main__":
    main()