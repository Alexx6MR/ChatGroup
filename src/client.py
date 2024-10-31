import socket
import threading
import time
import colorama


# Create the constants that will be used throughout the application
HOST: str = "127.0.0.1" # Server address -- localhost
PORT: int = 54321 # Server Port
buffer: int = 1024 # Temporary storage.
encoding: str = "utf-8" # Data encoding 8-bytes : ascii has 128-bytes.

# Ask the client to write his nickname
nickname:str = input("Choose a nickname: ").lower()

# Create variable to save client color
clientColor:str =""

# Function to connect to the server
def connect_to_server() -> socket.socket:
    global clientColor
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            client.connect((HOST, PORT))
            print()
            print("Connecting to server....")
            # save client color
            clientColor = client.recv(buffer).decode(encoding)
            return client
        except Exception as e:
            print(f"Could not connect to the server: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

# Create a client object
client = connect_to_server()

# Function to receive all message
def receive()->None:
    while True:
        try:
            message:str = client.recv(buffer).decode(encoding)
            if message == 'NICK':
                client.send(nickname.encode(encoding))
            else:
                print(f"{message} {colorama.Style.RESET_ALL}")
        except:
           print("An error occurred!")
           client.close()
           break

# Function to write a message
def write()->None:
    while True:
        try:
            message:str = f"{clientColor}{nickname}: {input()} "
            client.send(message.encode(encoding))
        except BrokenPipeError:
            print("The message cannot be sent, the server may be down.")
            break 


# Thread to allow the client receive message all the time
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Thread to allow the client send message all the time
write_thread = threading.Thread(target=write)
write_thread.start()