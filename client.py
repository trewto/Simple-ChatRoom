import socket
import threading

# Step 1: Connect to server
username = input("Enter your name: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5555))  # Connect to the server

# Step 2: Function to receive messages from server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'USERNAME':
                client_socket.send(username.encode('utf-8'))
            else:
                print(message)
        except:
            print("Connection error!")
            client_socket.close()
            break

# Step 3: Function to send messages to the server
def send_messages():
    while True:
        msg = f'{username}: {input("")}'
        client_socket.send(msg.encode('utf-8'))

# Step 4: Start receiving and sending threads
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
