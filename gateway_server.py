import socket
import threading
import subprocess
import json
from datetime import datetime

HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 9999       # Port for our gateway service

def get_system_info():
    """
    This function gathers the required system information.
    This is a suggested implementation. You can modify it if you wish.
    """
    # Get MAC Address for eth0 (a unique identifier for your device)
    try:
        mac_addr_output = subprocess.run(
            ['cat', '/sys/class/net/eth0/address'],
            capture_output=True, text=True, check=True
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        mac_addr_output = "MAC_NOT_FOUND"

    # Get system uptime
    try:
        uptime_output = subprocess.run(
            ['uptime', '-p'],
            capture_output=True, text=True, check=True
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        uptime_output = "UPTIME_NOT_FOUND"

    # Get current timestamp
    timestamp = datetime.now().isoformat()

    # Structure the data
    info = {
        "device_mac_address": mac_addr_output,
        "timestamp_utc": timestamp,
        "system_uptime": uptime_output
    }
    return info

def handle_client(conn, addr):
    """
    This function is executed in a separate thread for each client.
    """
    print(f"[NEW CONNECTION] {addr} connected.")
    with conn:
        while True:
            # Wait for a request from the client
            request = conn.recv(1024).decode('utf-8')
            if not request:
                # If client closes connection, break the loop
                break

            print(f"Received request from {addr}: {request}")

             ## --- TODO: YOUR CODE GOES HERE --- ##
            # 1. Check if the client's request is valid (e.g., is it "GET_DATA"?).
            if request.strip() == "GET_DATA":
                # 2. If the request is valid, call the get_system_info() function to get the data.
                system_data = get_system_info()
                # 3. Serialize the data into JSON string
                json_data = json.dumps(system_data)
                # 4. Encode and send the data back
                conn.sendall(json_data.encode('utf-8'))
            else:
                # 5. Handle invalid request
                error_msg = json.dumps({"error": "Invalid request. Use 'GET_DATA' to retrieve system information."})
                conn.sendall(error_msg.encode('utf-8'))
            ## --- END OF TODO --- ##

    print(f"[CONNECTION CLOSED] {addr} disconnected.")

def start_server():
    """
    Starts the main server loop to listen for incoming connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        # Create a new thread to handle the client connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
