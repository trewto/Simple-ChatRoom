import socket
import threading

# Step 1: Initialize the server
host = '0.0.0.0'  # Localhost
port = 5555  # Port to listen on
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

connected_clients = []
client_names = []

# Step 2: Function to send messages to all clients
def send_message_to_all(msg):
    for client in connected_clients:
        client.send(msg)

# Step 3: Handle communication with a single client
def manage_client(client):
    while True:
        try:
            # Get message from client
            message = client.recv(1024)
            send_message_to_all(message)
        except:
            # Remove client if there is an error (like disconnect)
            index = connected_clients.index(client)
            connected_clients.remove(client)
            client.close()
            name = client_names[index]
            send_message_to_all(f'{name} has left the chat.'.encode('utf-8'))
            client_names.remove(name)
            break

# Step 4: Function to accept new clients
def accept_clients():
    while True:
        client, address = server_socket.accept()
        print(f"New connection from {address}")

        # Request and save nickname
        client.send('USERNAME'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        client_names.append(username)
        connected_clients.append(client)

        print(f"Client's nickname is {username}")
        send_message_to_all(f"{username} joined the chat!".encode('utf-8'))
        client.send('You are now connected!'.encode('utf-8'))

        # Start a thread to manage this client
        thread = threading.Thread(target=manage_client, args=(client,))
        thread.start()

print("Chat server is live...")
accept_clients()
