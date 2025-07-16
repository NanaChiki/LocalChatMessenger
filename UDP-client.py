import socket
import os
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
    Main function to start the UDP client.

    This function initializes the client, binds it to a socket file, and waits for messages.
    It sends messages to the server and receives responses.
    """

    # Socket setup
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    server_address = '/tmp/udp_socket_file'
    client_address = '/tmp/udp_client_socket_file'


    # Create a loop that allows multiple messages without restarting
    try:
        # Cleanup any existing client socket file
        cleanup_socket_file(client_address)
        # Bind client socket file to the socket
        sock.bind(client_address)
        sock.settimeout(5.0) # Set timeout

        print("🚀 UDP Client started! Type 'quit' to exit.")

        message_counter = 1
        while True:
            message = input("Enter your message (or 'quit' to exit): ")
            if message.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break # This exists the while loop
            try:
                timestamp = get_timestamp()
                # Send message
                sock.sendto(message.encode(), server_address)
                print(f'📤 \033[92m[{timestamp}] Message #{message_counter} - Sending to Server: \033[0m{message}')
                # Increment message counter
                message_counter += 1 

                print('Waiting to receive...')
                # Receive 4096 bytes data at the maximum
                data, server = sock.recvfrom(4096)
                timestamp = get_timestamp()
                response = data.decode() # Show Data instead of b'Data'
                # Display the received data from the server
                print(f'📩 \033[94m[{timestamp}] Received: \033[0m {response} \n\033[94mServer address: \033[0m{server}')
    
            except socket.timeout:
                print("⚠️ Server did not respond within 5 seconds. Server might be down.")
                print("   Continue sending messages or type 'quit' to exit.")
                continue

            except Exception as e:
                print(f"❌ Error communicating with server: {e}")
                print("    Try again or type 'quit' to exit.")
                continue
    
    except KeyboardInterrupt:
        print("\n👋 Client interrupted by user")

    except ConnectionRefusedError:
        print("❌ Could not connect to server. Is the server running?")
    
    except Exception as e:
        print(f"❌ Fatal error: {e}")

    finally:
        # Cleanup
        sock.close()
        cleanup_socket_file(client_address)
        print('🧹 Cleanup completed')

if __name__ == "__main__":
    main()