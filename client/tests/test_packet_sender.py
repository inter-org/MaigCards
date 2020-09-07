import sys
from MaigCards.client.packet_sender import ClientPacketSender
from MaigCards.general.global_var import ClientThreadVar
import threading
import time
from MaigCards.client.client import *


game = Game()
test_player = Player("test")
game.join(test_player)
game.game_id = 2333


def getRandomCards():
    looptimes = random.randint(1, 5)
    res = []
    for i in range(0, looptimes):
        f = 1
        if f == 1:
            magic_list = list(map(int, MagicType))
            res.append(MagicCard(magic_list[random.randint(0, len(magic_list) - 1)]))
    return res


def makePackets():

    # for i in range(1, 100):
    f = random.randint(1, 5)

    if f == 1:
        byts = game.pick()

    if f == 2:
        game.player_index = random.randint(0, 6)
        byts = (game.act(random.randint(0, 6), getRandomCards()))

    if f == 3:
        byts = (game.skip())

    if f == 4:
        byts = (game.drop(getRandomCards()))

    if f == 5:
        byts = (game.throw())
    print("????") 
    return byts

def test_produce_packets():
    byts = makePackets()
    print("produce {}".format(byts))
    ClientThreadVar.putSendTop(byts)

    pass

def test_send_packets():
    client_packet_sender = ClientPacketSender('localhost', 2336, client_var=ClientThreadVar)
    client_packet_sender.connect()
    
    while not ClientThreadVar.readTermFlag():
        client_packet_sender.send()
    client_packet_sender.socket.close()

class ProduceThread(threading.Thread):
    def __init__(self, loop_count):
        threading.Thread.__init__(self)
        self.loop_count = loop_count
    
    def run(self):
        print("produce thread start")

        for i in range(0, self.loop_count):
            if ClientThreadVar.readTermFlag():
                print("exit produce thread")
                break
            print(i)
            test_produce_packets()
            time.sleep(1)

class SendThread(threading.Thread): 
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("send thread start")
        test_send_packets()
        print("send thread exit")


class ControlThread(threading.Thread):
    def __init__(self, sleep_time):
        threading.Thread.__init__(self)
        self.sleep_time = sleep_time


    def run(self):
        print("control thread start")
        time.sleep(self.sleep_time)
        print("control thread set term flag")
        ClientThreadVar.writeTermFlag(True)
        print("control thread exit")

threads = []

if __name__ == "__main__":
    thread1 = ProduceThread(100)
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

    
    

