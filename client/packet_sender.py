from general.packet_sender import PacketSenderBase


class ClientPacketSender(PacketSenderBase):
    def send(self):
        print("before getSendTop")
        bytes_ = self.client_var.getSendTop()
        print("after getSendTop")
        print(bytes_)
        if not (bytes_ is None):
            print("before sendall")
            self.socket.sendall(bytes_)
            print("after sendall")
