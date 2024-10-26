import socket
import threading


#* Create the constants that will be used throughout the application
HOST: str = "127.0.0.1" #* Server address -- localhost
PORT: int = 54321 #* Server Port
buffer: int = 1024 #* Temporary storage.
encoding: str = "utf-8" #* Data encoding 8-bytes : ascii has 128-bytes.


#* Ask the client to write his nickname
nickname = input("Choose a nickname: ").lower()

#* Create a client object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#* Connect to the server
client.connect((HOST, PORT))

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
        message = f"{nickname}: {input()}"
        client.send(message.encode(encoding))
        


#* Thread to allow the client receive message all the time
receive_thread = threading.Thread(target=receive)
receive_thread.start()

#* Thread to allow the client send message all the time
write_thread = threading.Thread(target=write)
write_thread.start()