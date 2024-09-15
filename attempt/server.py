# server.py
import socket
import threading

def handle_client(client_socket):
    while True:
        msg = client_socket.recv(1024).decode('utf-8')
        if not msg:
            break
        print(f"Received: {msg}")
        client_socket.send("Hello World".encode('utf-8'))
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8000))
    server.listen(5)
    print("Server started on port 8000")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

def stop_server(server):
    server.close()

if __name__ == "__main__":
    start_server()

