import socket
import threading


#* Create the constants that will be used throughout the application
HOST: str = "127.0.0.1" #* Server address -- localhost
PORT: int = 54321 #* Server Port
buffer: int = 1024 #* Temporary storage.
encoding: str = "utf-8" #* Data encoding 8-bytes : ascii has 128-bytes.

#* lists to be able to store clients and their nicknames
clientsList: list = [] 
nicknamesList: list = []


#* Function to send a message to every client except the client who sent it
def sendMessage(message: str, sender=None)->None:
    for client in clientsList:
        if client != sender:
            client.send(message)
  
  
  
#* Controls whether the user is still active or not to send a message        
def handle(client)->None:
    while True:
        try:
            message = client.recv(buffer)
            sendMessage(message=message, sender=client)
        except:
            index = clientsList.index(client)
            clientsList.remove(client)
            client.close()
            nickname = nicknamesList[index]
            sendMessage(f"{nickname} left the chat!".encode(encoding))
            nicknamesList.remove(nickname)
            break
  

#* the server starts here
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
   
    #* give the server an address and port and listen for clients
    server.bind((HOST, PORT))
    server.listen()
    print("Server is listening...")
    

    #* Loop to keep the server running
    while True:
        #* accept a client connection and get the client and the address
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        #* Send code (NICK) so that the client knows that he must give his nickname
        client.send("NICK".encode(encoding))
        
        #* get the user's nickname
        nickname: str = client.recv(buffer).decode(encoding)
       
        #* add the nickname to the nicknames list
        nicknamesList.append(nickname)
        
        #* add the client to the clients list
        clientsList.append(client)
        
        #* displaying a message to know the nickname of the client
        print(f"Nickname of the client is {nickname}!")
        
        #* send the message to everyone connected to the server
        sendMessage(f"{nickname} joined the chat!".encode(encoding))
        
        #* let the client know that it has connected to the server
        client.send("Connected to the server!".encode(encoding))
        sendMessage(f"actual clients: {len(clientsList)}".encode(encoding))

        #* creating a threat for each user that connects to the server, so they can send messages at the same time
        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()