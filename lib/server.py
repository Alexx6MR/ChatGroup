import socket
import threading
import logging
import colorama
from colorama import Fore, Style
import random


# Inicializar colorama
colorama.init()

# Configuración del logger
logging.basicConfig(
    level=logging.DEBUG,  # Cambia el nivel según sea necesario
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='log/server.log',  # Archivo donde se guardarán los logs
    filemode='a'  # Modo de apertura del archivo: 'a' para agregar
)

#* Create the constants that will be used throughout the application
HOST: str = "127.0.0.1" #* Server address -- localhost
PORT: int = 54321 #* Server Port
buffer: int = 1024 #* Temporary storage.
encoding: str = "utf-8" #* Data encoding 8-bytes : ascii has 128-bytes.

#* lists to be able to store clients and their nicknames
clientsList: list = [] 
nicknamesList: list = []
colorsList: list = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]  # Lista de colores
assignedColors: dict = {}  # Diccionario para almacenar colores asignados a usuarios

#* Function to send a message to every client except the client who sent it
def sendMessage(message: bytes, sender: socket.socket = None) -> None:
    for client in clientsList:
        if client != sender:
            client.send(message)

#* Controls whether the user is still active or not to send a message        
def handle(client: socket.socket) -> None:
    while True:
        try:
            message: bytes = client.recv(buffer)
            if not message:
                break
            sendMessage(message=message, sender=client)
            logging.info(f'Message receive and send to others clients: {message.decode(encoding)}')
        except Exception as e:
            logging.error(f'An error occurred: {e}')
            index: int = clientsList.index(client)
            clientsList.remove(client)
            client.close()
            nickname: str = nicknamesList[index]
            sendMessage(f"{nickname} left the chat!".encode(encoding))
            nicknamesList.remove(nickname)
            logging.info(f'Client disconnected: {nickname}')
            break

#* the server starts here
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    logging.info("Server is listening...")
    print("Server is listening...")

    #* Loop to keep the server running
    while True:
        #* accept a client connection and get the client and the address
        client, address = server.accept()
        logging.info(f'Connected with {str(address)}')
        print(f"Connected with {str(address)}")
        
        #* Send code (NICK) so that the client knows that he must give his nickname
        client.send("NICK".encode(encoding))
        
        #* get the user's nickname
        nickname: str = client.recv(buffer).decode(encoding)
        
        #* Asignar un color aleatorio al nuevo usuario
        color = random.choice(colorsList)
        if len(colorsList) > 0:
            color = random.choice(colorsList)
            colorsList.remove(color)  # Eliminar el color de la lista de colores disponibles
            assignedColors[nickname] = color 
       
        #* add the nickname to the nicknames list
        nicknamesList.append(nickname)
        
        #* add the client to the clients list
        clientsList.append(client)
        
        #* displaying a message to know the nickname of the client
        logging.info(f"Nickname of the client is {nickname}!")
        print(f"Nickname of the client is {nickname}!")
         
        client.send(" ".encode(encoding))
        #* let the client know that it has connected to the server
        client.send("**Connection to server successful***".encode(encoding))
        
        
        #* send the message to everyone connected to the server
        sendMessage(f"""
----------------------------------------
{color}{nickname} joined the chat!{Style.RESET_ALL} | actual clients: {len(clientsList)}
---------------------------------------- 
                    """.encode(encoding))
        
      
        
    

        #* creating a thread for each user that connects to the server
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
