import socket
import threading
import logging
from typing import List
import colorama


from config.logging.server_log_config import setupLogging
from config.theme.color import assignColor, recoverColor
from models.client_model import ClientModel

# Inicializar colorama
colorama.init()

# Configure the logger
setupLogging()



# lists to be able to store all the connected clients
clientsList: list[ClientModel] = [] 


# This function works like a broadcast and sends a message to all clients in the client list.
def broadcast(message: str, clientsList: List[ClientModel], sender: ClientModel = None) -> None:
    for client in clientsList[:]:  # Hacemos una copia de la lista para evitar problemas al modificarla
        if sender is None or client.address != sender.address:
            try:
                client.send(message)
            except Exception:
                logging.error(f"Error sending message to {client.nickname}. Removing client.")
                # Remueve el cliente si el envío falla
                clientsList.remove(client)
                recoverColor(client.color)
                client.close_socket()


# Controls whether the user is still active or not to send a message        
def handle(client: ClientModel) -> None:
    while True:
        try:
            message: str = client.recv();
            broadcast(clientsList=clientsList, message=message, sender=client)
            logging.info(f'Message receive and send to others clients: {message[5:]}')
        
        except ConnectionResetError as e:
            logging.error(f'Connection reset by peer for client: {client.nickname}')
            break 
        except Exception as e:
            logging.error(f'An error occurred: {e}')           
            if client in clientsList:
                recoverColor(client.color)
                clientsList.remove(client)
                client.close_socket()
            broadcast(clientsList=clientsList, message=f"{client.color}{client.nickname} left the chat!")
            logging.info(f'Client disconnected: {client.nickname}')
            break


# The server starts here
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(("127.0.0.1", 54321))
    server.listen()
    logging.info("Server is listening...")
    print("Server is listening...")

    # Loop to keep the server running
    while True:
        # Accept a client connection and get the client and the address
        client_socket, address = server.accept()
        
        # Create clientModel object
        client:ClientModel = ClientModel(client_socket=client_socket, address=address, color=assignColor())
        logging.info(f'Connected with {str(address)}')
        print(f"Connected with {str(address)}")
        
        # Send code (NICK) so that the client knows that he must give his nickname and set his color by default
        client.send(client.color)
        client.send("NICK")        
        
        # Set the nickname to the object client
        setattr(client, "nickname", client.recv()) 

        # Append the new client to the list of clients
        clientsList.append(client)
        
        # Displaying a message to know the nickname of the client
        logging.info(f"Nickname of the client is {client.nickname}!")
        print(f"Nickname of the client is {client.nickname}!")
         
        client.send(" ")
        client.send("***Connection to server successful***")
        
        # Send the message to everyone connected to the server
        broadcast(clientsList=clientsList, message=f"""
----------------------------------------
{client.color}{client.nickname} joined the chat! {colorama.Style.RESET_ALL} | actual clients: {len(clientsList)}
---------------------------------------- 
                """)
        
        # Creating a thread for each user that connects to the server
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()