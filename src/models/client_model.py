import socket
from core.utils.contants import encoding, buffer

class ClientModel:
    def __init__(self, client_socket: socket.socket, address:str, nickname: str = "", color: str = ""):
        self.address = address
        self.nickname = nickname
        self.color = color
        self.socket = client_socket
        
    def __str__(self):
        return f"Client(nickname={self.nickname}, address={self.address}, color={self.color})"
    
    # define the new send function of the client object
    def send(self, message: str = " ") -> None:
        try:
            if type(message) == bytes:
                self.socket.send(message)
            else:
                self.socket.send(message.encode(encoding))
        except ConnectionResetError as e:
               print(f"{self.nickname} left the chat!")
               self.socket.close()
    
    # define the new recv function of the client object
    def recv(self) -> str:
        try:
            return self.socket.recv(buffer).decode(encoding)
        except ConnectionResetError:
            print(f"{self.nickname} has been unexpectedly disconnected.")
            self.socket.close()
            return " "