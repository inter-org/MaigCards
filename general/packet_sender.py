import sys
import socket

class PacketSenderBase:
    def __init__(self, hostname, port, **kwargs):
        self.hostname = hostname
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_var = kwargs.get('client_var', None)
        self.server_var = kwargs.get('server_var', None)

       
    def connect(self):
        self.socket.connect((self.hostname, int(self.port)))
            


    def send(self):
        pass



