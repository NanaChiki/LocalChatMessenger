import socket
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


    # Create a loop that allows multiple messages without restarting
    try:
        # Cleanup any existing client socket file
        cleanup_socket_file(client_address)
        # Bind client socket file to the socket
        sock.bind(client_address)
        sock.settimeout(5.0) # Set timeout

        print("🚀 UDP Client started! Type 'quit' to exit.")

        while True:
            message = input("Enter your message (or 'quit' to exit): ")
            if message.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break # This exists the while loop
            try:
                # Send message
                timestamp = get_timestamp()
                sock.sendto(message.encode(), server_address)
                print(f'📤 [{timestamp}] Sending to Server: {message}')

                print('Waiting to receive...')
                # Receive 4096 bytes data at the maximum
                data, server = sock.recvfrom(4096)
                timestamp = get_timestamp()
                response = data.decode() # Show Data instead of b'Data'
                # Display the received data from the server
                print(f'📩 [{timestamp}] Received: {response}, Server address: {server}')
    
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