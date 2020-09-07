import sys
from MaigCards.client.packet_sender import ClientPacketSender
from MaigCards.general.global_var import ClientThreadVar
import threading
import time

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
    game = Game()
    test_player = Player("test")
    game.join(test_player)
    game.game_id = 2333



    for i in range(1, 100):
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
    return byts

def test_produce_packets():
    ClientThreadVar.putSendTop(makePackets())
    pass

def test_send_packets():
    client_packet_sender = ClientPacketSender('localhost', 2333)    
    client_packet_sender.connect()
    
    while not ClientThreadVar.readTermFlag():
        byts = ClientThreadVar.getSendTop()
        if not byts == None:
            client_packet_sender.send(byts)
            print("sent {}".format(byts))

class ProduceThread(threading.Thread):
    def __init__(self, loop_count):
        threading.Thread.__init__(self)
        self.loop_count = loop_count
    
    def run(self):
        for i in range(0, self.loop_count):
            if not ClientThreadVar.readTermFlag():
                break
            test_product_packets()


class SendThread(threading.Thread): 
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        test_send_packets()


class ControlThread(threading.Thread):
    def __init__(self, sleep_time):
        threading.Thread.__init__(self)
        self.sleep_time = sleep_time


    def run(self):
        time.sleep(self.sleep_time)
        ClientThreadVar.writeTermFlag(True)

threads = []

if __name__ == "__main__":
    thread1 = ProduceThread(100)
    thread2 = SendThread()
    thread3 = ControlThread(3)
    thread1.start()
    thread2.start()
    thread3.start()
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)

    for thread in threads:
        thread.join()

    
    

