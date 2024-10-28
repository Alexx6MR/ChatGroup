import socket
import threading
import time

import colorama
from  core.utils.contants import HOST, PORT, buffer, encoding
from models.client_model import ClientModel



#* Ask the client to write his nickname
nickname = input("Choose a nickname: ").lower()

#* Function to connect to the server
def connect_to_server() -> socket.socket:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            client.connect((HOST, PORT))
            print()
            print("Connecting to server....")
            color = client.recv(buffer).decode(encoding)
            return ClientModel(client_socket=client, nickname=nickname, address=client.getsockname, color=color)
        except Exception as e:
            print(f"Could not connect to the server: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

#* Create a client object
client = connect_to_server()

#* Function to receive all message
def receive()->None:
    while True:
        try:
            message = client.recv()
            if message == 'NICK':
                client.send(nickname.encode(encoding))
            else:
                print()      
                print(f"{"" if "*" in message else " " * 40} {message} {colorama.Style.RESET_ALL}")
                print()
        except:
           print("An error occurred!")
           client.close()
           break



#* Function to write a message
def write()->None:
    while True:
        try:
            message = f"{client.color}{nickname}: {input()} "
            client.send(message.encode(encoding))
        except BrokenPipeError:
            print("The message cannot be sent, the server may be down.")
            break 


#* Thread to allow the client receive message all the time
receive_thread = threading.Thread(target=receive)
receive_thread.start()

#* Thread to allow the client send message all the time
write_thread = threading.Thread(target=write)
write_thread.start()