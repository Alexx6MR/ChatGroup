import socket
import threading
import time

#* Create the constants that will be used throughout the application
HOST: str = "127.0.0.1" #* Server address -- localhost
PORT: int = 54321 #* Server Port
buffer: int = 1024 #* Temporary storage.
encoding: str = "utf-8" #* Data encoding 8-bytes : ascii has 128-bytes.


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
            return client
        except Exception as e:
            print(f"No se pudo conectar al servidor: {e}")
            print("Reintentando en 5 segundos...")
            time.sleep(5)

#* Create a client object
client = connect_to_server()

#* Function to receive all message
def receive()->None:
    while True:
        try:
            message = client.recv(buffer).decode(encoding)
            if message == 'NICK':
                client.send(nickname.encode(encoding))
            else:
                print(message)
                
        except:
           print("An error occurred!")
           client.close()
           break



#* Function to write a message
def write()->None:
    while True:
        try:
            message = f"{nickname}: {input()}"
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