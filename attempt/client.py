# client.py

import os
import socket

def get_server_url():
    # Retrieve SERVER_URL from environment variables
    server_url = os.getenv('SERVER_URL', 'localhost:8000')
    
    # Check if SERVER_URL is not set
    if not server_url:
        raise ValueError("The 'SERVER_URL' environment variable is not set.")
    print("env: server_url=" + str(server_url))  
    return server_url


def send_message(message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_uri = get_server_url()
    client.connect((s_uri, 8000))
    client.send(message.encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    print(f"Response from server: {response}")
    client.close()

if __name__ == "__main__":
    send_message("Hello Server")

