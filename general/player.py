import gameinfo
import random



class Player:
    __slots__ = ('gem_cards', 'magic_cards', 'treasure_cards', 'level')
    def __init__(self, name):
        self.id = name 
        self.level = 1
        self.gem_cards = list()
        self.magic_cards = list()
        self.treasure_cards = list()

        self._initPlayer()



