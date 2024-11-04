import logging
import socket


class ClientModel:
    def __init__(self, client_socket: socket.socket, address:str, nickname: str = "", color: str = ""):
        self.address = address
        self.nickname = nickname
        self.color = color
        self.socket = client_socket
        self.buffer = 1024
        self.encoding = "utf-8" # Data encoding 8-bytes : ascii has 128-bytes.
        
    def __str__(self):
        return f"Client(nickname={self.nickname}, address={self.address}, color={self.color})"
    
    # define the new send function of the client object
    def send(self, message: str = " ") -> None:
        if type(message) == bytes:
            self.socket.send(message)
        else:
            self.socket.send(message.encode(self.encoding))
      
    
    # define the new recv function of the client object
    def recv(self) -> str:
        try:
            return self.socket.recv(self.buffer).decode(self.encoding)
        except ConnectionResetError:
            print(f"{self.nickname} has been unexpectedly disconnected.")
            self.close_socket()
            return " "
    
    # Make sure to close the socket correctly
    def close_socket(self) -> None:
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                logging.error(f"Error closing socket for client {self.nickname}: {e}")
            finally:
                self.socket = None # Ensures that the socket is not reused 