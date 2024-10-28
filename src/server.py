import socket
import threading
import logging
import colorama


from config.logging.server_log_config import setupLogging
from core.utils.contants import HOST, PORT
from core.utils.messaging import broadcast
from config.theme.color import assignColor, recoverColor
from models.client_model import ClientModel

# Inicializar colorama
colorama.init()

# Configure the logger
setupLogging()



# lists to be able to store clients and their nicknames
clientsList: list[ClientModel] = [] 


# Controls whether the user is still active or not to send a message        
def handle(client: ClientModel) -> None:
    while True:
        try:
            message: str = client.recv();
            broadcast(clientsList=clientsList, message=message, sender=client)
            logging.info(f'Message receive and send to others clients: {message}')
        
        except ConnectionResetError as e:
            logging.error(f'Connection reset by peer for client: {client.nickname}')
            break 
        except Exception as e:
            logging.error(f'An error occurred: {e}')           
            if client in clientsList:
                recoverColor(client.color)
                clientsList.remove(client)
                
            client.socket.close()
            broadcast(clientsList=clientsList, message=f"{client.color} {client.nickname} left the chat!")
            logging.info(f'Client disconnected: {client.nickname}')
            break


# The server starts here
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    logging.info("Server is listening...")
    print("Server is listening...")

    # Loop to keep the server running
    while True:
        # accept a client connection and get the client and the address
        client_socket, address = server.accept()
        
        # create clientModel object
        client = ClientModel(client_socket=client_socket, address=address, color=assignColor())
        logging.info(f'Connected with {str(address)}')
        print(f"Connected with {str(address)}")
        
        # Send code (NICK) so that the client knows that he must give his nickname and set his color by default
        client.send(client.color)
        client.send("NICK")        
        
        # set the nickname to the object client
        setattr(client, "nickname", client.recv()) 

        # append the new client to the list of clients
        clientsList.append(client)
        
        # displaying a message to know the nickname of the client
        logging.info(f"Nickname of the client is {client.nickname}!")
        print(f"Nickname of the client is {client.nickname}!")
         
        client.send(" ")
        client.send("***Connection to server successful***")
        
        
        # send the message to everyone connected to the server
        broadcast(clientsList=clientsList, message=f"""
----------------------------------------
{client.color}{client.nickname} joined the chat! {colorama.Style.RESET_ALL} | actual clients: {len(clientsList)}
---------------------------------------- 
                """)
        
        # creating a thread for each user that connects to the server
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()