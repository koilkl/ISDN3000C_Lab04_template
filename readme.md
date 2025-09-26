# System Monitoring Client-Server Application

This is a simple client-server application for monitoring device system information. The server collects the device's MAC address, system uptime, and current timestamp, while the client sends requests to the server periodically and retrieves this information.


## Features

- **Server (gateway_server.py)**: Listens on a specified port, receives client requests, collects system information (MAC address, uptime, UTC timestamp), and returns it in JSON format to the client.
- **Client (monitoring_client.py)**: Connects to the server regularly, sends data requests, receives and parses the returned system information, and displays it.


## Requirements

- Python 3.x (no additional dependencies required, uses standard libraries)
- The server and client must be on the same network (or able to access each other over the network)


## Configuration Instructions

### Server Configuration (gateway_server.py)

The default configuration meets basic needs. To modify, adjust the following parameters:HOST = '0.0.0.0'  # Listens on all available network interfaces
PORT = 9999       # Service port
### Client Configuration (monitoring_client.py)

Modify the following parameters according to the actual server address:SERVER_IP = '192.168.127.10'  # Server IP address (replace with actual server IP)
SERVER_PORT = 9999            # Server port (must match the server's port)
REQUEST_MESSAGE = "GET_DATA"  # Request command (must match the server's expected command)

## Running Steps

1. **Start the Server**  
   Run on the server device:
   ```bash
   python3 gateway_server.py
   ```
   After successful startup, it will display: `[LISTENING] Server is listening on 0.0.0.0:9999`

2. **Start the Client**  
   Run on the client device (ensure the server IP is configured correctly):
   ```bash
   python3 monitoring_client.py
   ```
   The client will send a request to the server every 60 seconds and display the retrieved system information.


## Function Details

- **Server Information Collection**:
  - Device MAC address (obtained via the `eth0` network interface)
  - System uptime (obtained via the `uptime -p` command)
  - Current UTC timestamp (ISO format)

- **Client Behavior**:
  - Attempts to connect to the server every 60 seconds
  - Sends a `GET_DATA` request to obtain information
  - Automatically parses JSON responses and displays them in a user-friendly format
  - Handles exceptions such as connection failures and non-JSON responses

- **Multi-Client Support**: The server uses multi-threading to handle multiple client requests simultaneously.


## Common Issues

1. **Connection Failure**:
   - Check if the server is running
   - Verify that the server IP and port are configured correctly
   - Test network connectivity between the server and client (use the `ping` command)

2. **MAC Address Shows "MAC_NOT_FOUND"**:
   - The server device may not have an `eth0` network interface. Modify the network interface name in the `get_system_info` function (e.g., change to `wlan0`).

3. **Uptime Shows "UPTIME_NOT_FOUND"**:
   - The server device may not support the `uptime -p` command. Modify the information collection method in the `get_system_info` function.
