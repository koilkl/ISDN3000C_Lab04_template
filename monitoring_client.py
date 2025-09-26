import socket
import time
import json

# --- TODO: Configure these values --- #
SERVER_IP = '192.168.127.10'  # The IP address of your RDK-X5
SERVER_PORT = 9999
REQUEST_MESSAGE = "GET_DATA" # The message your server expects
# --- END OF TODO --- #

def run_client():
    while True:
        print("-" * 30)
        print(f"Attempting to connect to {SERVER_IP}:{SERVER_PORT}...")
        try:
            # --- TODO: YOUR CODE GOES HERE --- #
            # 1. Create a socket object (IPv4, TCP)
            # 2. Use 'with' statement for automatic cleanup
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # 3. Connect to the server
                s.connect((SERVER_IP, SERVER_PORT))
                print("Connected to the server.")
                
                # 4. Send the REQUEST_MESSAGE, encoded to bytes
                s.sendall(REQUEST_MESSAGE.encode('utf-8'))
                print(f"Sent request: {REQUEST_MESSAGE}")
                
                # 5. Receive the response from the server (up to 4096 bytes)
                response = s.recv(4096)
                
                if not response:
                    print("No data received from server.")
                    continue
                
                # 6. Decode the response from bytes to string
                response_str = response.decode('utf-8')
                
                # 7. Parse JSON string into a dictionary (handle potential parsing errors)
                try:
                    data = json.loads(response_str)
                    # 8. Print received data in user-friendly format
                    print("Received system information:")
                    for key, value in data.items():
                        print(f"  - {key}: {value}")
                except json.JSONDecodeError:
                    print(f"Received non-JSON response: {response_str}")
            # --- END OF TODO --- #

        except ConnectionRefusedError:
            print("Connection failed. Is the server running?")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Wait for 60 seconds before the next request
        print("\nWaiting for 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    run_client()
