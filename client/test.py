from client import Game, Packet
import sys
sys.path.append("..")
from general.player import Player
from general.gameinfo import *
import random
from server.server import *


def getRandomCards():
    looptimes = random.randint(1, 5)
    res = []
    for i in range(0, looptimes):
        f = 1
        if f == 1:
            magic_list = list(map(int, MagicType))
            res.append(MagicCard(magic_list[random.randint(0, len(magic_list) - 1)]))
    return res
            

def test(): 
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
            print("change the player_index to {}".format(game.player_index))
            byts = (game.act(random.randint(0, 6), getRandomCards()))

        if f == 3:
            byts = (game.skip())

        if f == 4:
            byts = (game.drop(getRandomCards()))

        if f == 5:
            byts = (game.throw())
        print(Server.unserialize(byts))

if __name__ == '__main__':
    test()

