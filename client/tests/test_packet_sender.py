import threading
import time

from client.client import *
from client.packet_sender import ClientPacketSender
from general.gameinfo import *
from general.global_var import ClientThreadVar
from general.player import Player
import socket



def get_random_cards():
    looptimes = random.randint(1, 5)
    res = []
    for i in range(0, looptimes):
        f = 1
        if f == 1:
            magic_list = list(map(int, MagicType))
            res.append(MagicCard(magic_list[random.randint(0, len(magic_list) - 1)]))

    return res

def make_packets():
    game = Game()
    test_player = Player("test")
    game.join(test_player)
    game.game_id = 2333
    # for i in range(1, 100):
    f = random.randint(1, 5)
    byts = bytes()
    if f == 1:
        byts = game.pick()

    if f == 2:
        game.player_index = random.randint(0, 6)
        byts = (game.act(random.randint(0, 6), get_random_cards()))

    if f == 3:
        byts = (game.skip())

    if f == 4:
        byts = (game.drop(get_random_cards()))

    if f == 5:
        byts = (game.throw())
    return byts

class ProduceThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global ClientThreadVar
        i = int()
        while not ClientThreadVar.readTermFlag():
            byts = make_packets()
            i = i + 1
            ClientThreadVar.putSendTop(byts)

        print("exit produce thread, {} packets are maked".format(i))


class SendThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global ClientThreadVar
        packet_sender = ClientPacketSender('localhost', 2555, client_var=ClientThreadVar)
        packet_sender.connect()
        # connect to the server


        i = 0
        # get the qsize
        while not ClientThreadVar.readTermFlag():
            bytes_to_send = ClientThreadVar.getSendTop()
            if bytes_to_send is None:
                time.sleep(0.01)
                continue
            packet_sender.socket.sendall(bytes_to_send)
            i += 1


        qsize = packet_sender.client_var.getSendQsize()
        while qsize > 0:
            bytes_to_send = ClientThreadVar.getSendTop()
            packet_sender.socket.sendall(bytes_to_send)
            i += 1
            qsize = packet_sender.client_var.getSendQsize()

        print("send thread exit, sent {} packets.".format(i))






class ControlThread(threading.Thread):
    def __init__(self, sleep_time):
        threading.Thread.__init__(self)
        self.sleep_time = sleep_time

    def run(self):
        global ClientThreadVar
        time.sleep(self.sleep_time)
        ClientThreadVar.writeTermFlag(True)
        print("exit control thread")

threads = []

if __name__ == "__main__":
    thread1 = ProduceThread()
    thread2 = SendThread()
    thread3 = ControlThread(10)
    thread1.start()
    thread2.start()
    thread3.start()
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)

    for thread in threads:
        thread.join()
    print("all threads return")
