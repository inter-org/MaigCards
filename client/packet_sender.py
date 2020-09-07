import sys
import socket
from MaigCards.general.packet_sender import PacketSenderBase

class ClientPacketSender(PacketSenderBase):
    def send(self):
        bytes_ = self.client_var.getSendTop()
        self.socket.sendall(bytes_)
        

