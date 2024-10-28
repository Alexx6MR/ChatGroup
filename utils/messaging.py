import socket
from typing import List

def send_message(message: bytes, clientsList: List[socket.socket], sender: socket.socket = None) -> None:
    for client in clientsList:
        if client != sender:
            client.send(message)
