# models/client.py
class Client:
    def __init__(self, socket, nickname, color):
        self.socket = socket
        self.nickname = nickname
        self.color = color
