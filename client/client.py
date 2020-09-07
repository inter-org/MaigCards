#!/usr/bin/python
# -*- coding:UTF-8 -*-

import sys
from enum import IntEnum
from MaigCards.general.player import Player
from MaigCards.general.gameinfo import *
import random
import socket

def throw()->int:
    return [gameinfo.DiceChoice.RED, gameinfo.DiceChoice.RED, gameinfo.DiceChoice.BLUE, gameinfo.DiceChoice.BLUE, gameinfo.DiceChoice.GREEN, gameinfo.DiceChoice.BLACK, gameinfo.DiceChoice.WHITE, gameinfo.DiceChoice.PURPLE] [random.randint(0, 7)]

class GameStatus(IntEnum):
    PREPARING=0x0
    STARTED=0x1
    FINISHED=0x2
    SUSPEND=0x3

MAX_PLAYER=6

# # 
# class GlobalVar:
#     packets_send_lock = threading.Lock()
#     packets_send = Queue()
#     packets_recv_lock = threading.Lock()
#     packets_recv = Queue()
# 
#     @staicmethod
#     def getPackets2Send():
#         return GlobalVar.packets_send
# 
#     @staticmethod
#     def getPacketsRecv():
#         return GlobalVar.packets_recv
# 


# 游戏封包说明：
# 这个游戏封包不会特别大，所以不需要分包之类的操作，下面说一说包的数据结构
# 2B gameinfo.PacketType
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
        self.game_id = 0
        if type_ == gameinfo.PacketType.PICK:
            self.pick_type = gameinfo.CardType.GEM

        elif type_ == gameinfo.PacketType.ACT:
            self.target = ""
            self.num_of_cards = 0
            self.cards = []


        elif type_ == gameinfo.PacketType.DROP:
            self.num_of_cards = 0
            self.cards = []


    def serialize(self):
        # print("type={}".format(self.type))
        res_bytes = bytes()
        type_b = (self.type).to_bytes(1, byteorder='big')
        performer_b = (self.performer).to_bytes(1, byteorder='big')
        gameid_b = (self.game_id).to_bytes(2, byteorder='big')

        # print("{}:{}:{}".format(type_b, performer_b, gameid_b))


        res_bytes = type_b + performer_b + gameid_b
        # print("res: {}".format(res_bytes))
        # print("len: {} : {} {}".format(len(res_bytes), res_bytes[0:0], int.from_bytes([res_bytes[0]], 'big')))
        # v = memoryview(res_bytes)
        # print("gameid: {} : {}".format(int.from_bytes(gameid_b,'big'), int.from_bytes(res_bytes[2:3], 'big')))
        extra_bytes = bytes()

        if self.type == gameinfo.PacketType.PICK:
            extra_bytes = extra_bytes + (int(self.pick_type).to_bytes(1, byteorder='big'))

        elif self.type == gameinfo.PacketType.ACT:
            extra_bytes = extra_bytes + (int(self.target).to_bytes(1, byteorder='big'))

        if self.type == gameinfo.PacketType.ACT or self.type == PacketType.DROP:
            extra_bytes = extra_bytes + (int(self.num_of_cards).to_bytes(2, byteorder='big'))
            for i in range(0, self.num_of_cards):
                extra_bytes = extra_bytes + (int(self.cards[i].type).to_bytes(1, byteorder='big'))
                extra_bytes = extra_bytes + (int(self.cards[i].getType()).to_bytes(2, byteorder='big'))

        return res_bytes + extra_bytes


class Game:
    def __init__(self):
        self.players = list()
        self.game_id = 0
        self.round_count = 0
        self.action_list = list()
        self.gem_cards_pile = list()
        self.magic_cards_pile = list()
        self.treasure_cards_pile = list()

        self.player_index = 0

     
    def join(self, player_: Player):
        if len(self.players) >= MAX_PLAYER:
            return (0, "full")

        self.players.append(player_)

    '''
    下面五个方法一律返回bytearray()
    欢迎完善
    '''
    def pick(self): # 当前index为player_index的玩家抽卡
        packet = Packet(gameinfo.PacketType.PICK)
        packet.performer = self.player_index
        packet.game_id = self.game_id
        return packet.serialize()

    def act(self, target_index, cards: list): # 打出卡片
        packet = Packet(gameinfo.PacketType.ACT)
        packet.performer = self.player_index
        packet.game_id = self.game_id
        packet.target = target_index
        packet.num_of_cards = len(cards)
        packet.cards = cards
        return packet.serialize()

    def skip(self): # 跳过或者结束当前回合
        packet = Packet(gameinfo.PacketType.SKIP)
        packet.performer = self.player_index
        packet.game_id = self.game_id
        return packet.serialize()

    def drop(self, cards: list): # 弃牌
        packet = Packet(gameinfo.PacketType.DROP)
        packet.performer = self.player_index
        packet.game_id = self.game_id
        packet.num_of_cards = len(cards)
        packet.cards = cards
        return packet.serialize()

    def throw(self): # 投骰子
        packet = Packet(gameinfo.PacketType.THROW)
        packet.performer = self.player_index
        packet.game_id = self.game_id
        return packet.serialize()
     

    @property
    def status(self):
        return self.status

    @property
    def gameID(self):
        return game_id

    @property
    def roundCount(self):
        return self.round_count

    

