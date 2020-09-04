#!/usr/bin/python
# -*- coding:UTF-8 -*-

from enum import IntEnum
from general import gameinfo, player
import random



def throw()->int:
    return [gameinfo.DiceChoice.RED, gameinfo.DiceChoice.RED, gameinfo.DiceChoice.BLUE, gameinfo.DiceChoice.BLUE, gameinfo.DiceChoice.GREEN, gameinfo.DiceChoice.BLACK, gameinfo.DiceChoice.WHITE, gameinfo.DiceChoice.PURPLE] [random.randint(0, 7)]

class PacketType(IntEnum):
    PICK=0x01
    ACT=0x02
    SKIP=0x03
    DROP=0x04

class GameStatus(IntEnum):
    PREPARING=0x0
    STARTED=0x1
    FINISHED=0x2
    SUSPEND=0x3

MAX_PLAYER=6


class Packet:
    def __init__(self, type_: PacketType):
        self.performer = ""
        if type_ == PacketType.PICK:
            self.pick_type = gameinfo.CardType.GEM

        elif type_ == PacketType.ACT:
            self.target = ""
            self.num_of_cards = 0
            self.cards = []


        elif type_ == PacketType.DROP:
            self.num_of_cards = 0
            self.cards = []


    def serialize():
        pass


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
     

    @property
    def status(self):
        return self.status

    @property
    def gameID(self):
        return game_id

    @property
    def roundCount(self):
        return self.round_count



