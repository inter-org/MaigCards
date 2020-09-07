import random



class Player:
    __slots__ = ('id', 'name', 'gem_cards', 'magic_cards', 'treasure_cards', 'level')
    def __init__(self, name):
        self.id = 0
        self.name = name 
        self.level = 1
        self.gem_cards = list()
        self.magic_cards = list()
        self.treasure_cards = list()

    

