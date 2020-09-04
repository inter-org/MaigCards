#!/usr/bin/python
# -*- coding:UTF-8 -*-

from enum import IntEnum
from general import gameinfo, player
import random
import pickle



def throw()->int:
    return [gameinfo.DiceChoice.RED, gameinfo.DiceChoice.RED, gameinfo.DiceChoice.BLUE, gameinfo.DiceChoice.BLUE, gameinfo.DiceChoice.GREEN, gameinfo.DiceChoice.BLACK, gameinfo.DiceChoice.WHITE, gameinfo.DiceChoice.PURPLE] [random.randint(0, 7)]

class PacketType(IntEnum):
    PICK=0x01
    ACT=0x02
    SKIP=0x03
    DROP=0x04
    THROW=0x05

class GameStatus(IntEnum):
    PREPARING=0x0
    STARTED=0x1
    FINISHED=0x2
    SUSPEND=0x3

MAX_PLAYER=6

# 游戏封包说明：
# 这个游戏封包不会特别大，所以不需要分包之类的操作，下面说一说包的数据结构
# 2B PacketType
# 2B gameid
# 1B performer
'''
上面的8B是必须字节，表示了动作的类型已经动作的发出者
下面说根据不同的包类型需要的额外字节
PICK:
    1B pick_type 

ACT:
    1B target
    2B num_of_cards
    (num_of_cards * 3)B cards

DROP:
    2B num_of_cards
    (num_of_cards * 3)B cards

SKIP&THROW:
    无额外字节
'''
class Packet:
    def __init__(self, type_: PacketType):
        self.type = type_
        self.performer = 0
        self.gameid = 0
        if type_ == PacketType.PICK:
            self.pick_type = gameinfo.CardType.GEM

        elif type_ == PacketType.ACT:
            self.target = ""
            self.num_of_cards = 0
            self.cards = []


        elif type_ == PacketType.DROP:
            self.num_of_cards = 0
            self.cards = []


    def serialize(self):
        res_bytes = bytearray()
        type_b = (self.type).to_bytes(1, byteorder='big')
        performer_b = (self.performer).to_bytes(1, byteorder='big')
        gameid_b = (self.gameid).to_bytes(2, byteorder='big') 
         
        res_bytes.append(type_b).append(performer_b).append(gameid_b)
        extra_bytes = bytearray()

        if type_ == PacketType.PICK:
            extra_bytes.append(int(self.pick_type).to_bytes(1, byteorder='big'))

        elif type_ == PacketType.ACT:
            extra_bytes.append(int(self.target).to_bytes(1, byteorder='big'))
        
        if type_ == PacketType.ACT pr type_ == PacketType.DROP:
            extra_bytes.append(int(self.num_of_cards).to_bytes(2, byteorder='big'))
            for i in range(0, self.num_of_cards):
                extra_bytes.append(int(self.cards[i].type).to_bytes(1, byte_order='big'))
                extra_bytes.append(int(self.cards[i].getType().to_bytes(2, byte_order='big'))

        return res_bytes + extra_bytes

class Game:
    def __init__(self):
        self.players = list()
        self.status = 0
        self.game_id = 0
        self.round_count = 0
        self.action_list = list()
        self.gem_cards_pile = list()
        self.magic_cards_pile = list()
        self.treasure_cards_pile = list()

        self.player_index = 0

     
    def join(self, player_: player.Player)->tuple(int, str):
        if len(players) >= MAX_PLAYER:
            return (0, "full")

        self.players.append(player_)

    '''
    下面五个方法一律返回bytearray()
    欢迎完善
    '''
    def pick(self): # 当前index为player_index的玩家抽卡
        pass


    def act(self, target_index, cards: list): # 打出卡片
        pass

    def skip(self): # 跳过或者结束当前回合
        pass

    def drop(self, cards: list): # 弃牌
        pass

    def throw(self): # 投骰子
        pass
     

    @property
    def status(self):
        return self.status

    @property
    def gameID(self):
        return game_id

    @property
    def roundCount(self):
        return self.round_count

    

