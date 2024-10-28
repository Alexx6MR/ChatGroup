from typing import List

from models.client_model import ClientModel

# This function works like a broadcast and sends a message to all clients in the client list.
def broadcast(message: str, clientsList: List[ClientModel], sender: ClientModel = None) -> None:
    
    for client in clientsList: 
        if sender is None or client.address != sender.address:
            client.send(message)
