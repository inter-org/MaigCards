from enum import IntEnum



class GemColor(IntEnum):
    RED=0x01
    GREEN=0x02
    BLUE=0x03
    BLACK=0x04
    WHITE=0x05

class DiceChoice(IntEnum):
    RED=0x01
    GREEN=0x02
    BLUE=0x03
    BLACK=0x04
    WHITE=0x05
    PURPLE=0x06

GemColorNames = ["RED", "GREEN", "BLUE", "BLACK", "WHITE"]
# format of DICE
# 0x PURPLE RED GREEN BLUE BLACK WHITE
DICE = 0x121211

class CardType(IntEnum):
    GEM=0x01
    MAGIC=0x02
    TREASURE=0x03

class MagicType(IntEnum):
    RED_COPY=0x1001
    GREEN_COPY=0x1002
    BLUE_COPY=0x1003
    BLACK_COPY=0x1004
    WHITE_COPY=0x1005

    RED_EPURATE=0x2001
    GREEN_EPURATE=0x2002
    BLUE_EPURATE=0x2003
    BLACK_EPURATE=0x2004
    WHITE_EPURATE=0x2005

    RED_SUMMON=0x3001
    GREEN_SUMMON=0x3002
    BLUE_SUMMON=0x3003
    BLACK_SUMMON=0x3004
    WHITE_SUMMON=0x3005

    SPEC_REPLACE=0x4001    

    NON_CONSUME=0x5001

class TreasureType(IntEnum):
    DESPOIL=0x0001
    SHIELDER=0x0002
    GIFT=0x0003
    EXCHANGE=0x0004
    FORGE=0x0005

TreasureNames=[
        '掠夺',
        '庇护',
        '恩赐',
        '交换',
        '合成'
]

TreasureNamesEn = [
        'Despoil',
        'Shielder',
        'Gift',
        'Exchange',
        'Forge'
]


class Card: 
    __slots__ = ('type', 'name')
    def __init__(self, type_: CardType, name): 
        self.type = type_
        self.name = name
    
class GemCard(Card):
    def __init__(self, color: GemColor):
        Card.__init__(self, CardType.GEM, GemColorNames[color - 1])
    
    @staticmethod
    def isAdvanced(color: GemColor):
        return not(color == GemColor.RED or color == GemColor.BLUE)
    
    def isAdvanced(self):
        return GemCard.isAdvanced(self.color)
    


class MagicCard(Card):
    __slots__ = ('magictype', 'demand', 'level')
    def __init__(self, magictype: MagicType, demand):
        Card.__init__(self, CardType.MAGIC, getMagicName(magictype))
        self.magictype = magictype
        self.demand = demand
        self.level = getMagicLevel(magictype, demand)
    
    @staticmethod
    def isCopyMagic(magictype):
        return magictype & 0x1FFF == magictype 

    @staticmethod
    def isEpurateMagic(magictype):
        return magictype & 0x2FFF == magictype 
    
    @staticmethod
    def isSummonMagic(magictype):    
        return magictype & 0x3FFF == magictype 

    @staticmethod
    def isSpecialMagic(magictype):
        return magictype & 0x4FFF == magictype 
    
    @staticmethod
    def isConsumeMagic(magictype):
        return magictype & 0x5FFF == magictype

    @staticmethod
    def getMagicName(type_: MagicType):
        if type_ == MagicType.SPEC_REPLACE:
            return "等价交换"

        if type_ == MagicType.NON_CONSUME:
            return "凑等级卡"

        colorNames = ["红", "绿", "蓝", "黑", "白"]
        magicTypeNames = ["复制术", "提炼术", "召唤术"]

        return colorNames[(type_ & 0x000F) - 1] + "宝石" + magicTypeNames[((type_ & 0xF000) >> 12) - 1]


    @staticmethod
    def getDemand(magictype: MagicType):
        target_gem = GemColor(magictype & 0x000F)
        demand = 0x00000

        if MagicCard.isCopyMagic(magictype):
           for i in list(map(int, GemColor)):
                offset = (GemColor.WHITE - i) * 4
                if i == target_gem:
                    dice = ((0xF << offset) & DICE) >> offset
                    demand |= (2 + (2-dice)) << offset
                elif i == GemColor.RED or i == GemColor.BLUE:
                    demand |= 1 << offset

        elif MagicCard.isEpurateMagic(magictype):
            for i in list(map(int, GemColor)):
                offset = (GemColor.WHITE - i) * 4
                if i == target_gem:
                    demand |= 2 << offset             
                elif i == GemColor.WHITE or i == GemColor.BLACK:
                    demand |= 1 << offset

        elif MagicCard.isSummonMagic(magictype):
            for i in list(map(int, GemColor)):
                offset = (GemColor.WHITE - i) * 4
                if i == target_gem or i == GemColor.GREEN:
                    demand |= 2 << offset
                elif i == GemColor.BLACK or i == GemColor.WHITE:
                    demand |= 1 << offset

        elif MagicCard.isConsumeMagic(magictype):        
            for i in list(map(int, GemColor)):
                offset = (GemColor.WHITE - i) * 4
                if i == GemColor.RED or i == GemColor.BLUE:
                    demand |= 2 << offset

        elif magictype == MagicType.SPEC_REPLACE:
            demand = 0x11111



        return demand


    @staticmethod
    def getDemandString(demand):
        str_msg = ""
        gem_names = ["红宝石", "绿宝石", "蓝宝石", "黑宝石", "蓝宝石"]
        for base in list(map(int, GemColor)):
            offset = (GemColor.WHITE - base) * 4
            require = (demand & (0xF << offset)) >> offset
            str_msg = str_msg + ((gem_names[base - 1] + "*" + str(require) + " ") if require != 0 else "")

        return str_msg





    # format of demand
    # GEMTYPE  RED GREEN BLUE BLACK WHITE
    #        0x n1  n2    n3   n4    n5
    # example: 0x54321 means take...
    @staticmethod
    def getMagicLevel(magictype: MagicType, demand):
        if MagicCard.isCopyMagic(magictype):
            return 1

        elif MagicCard.isEpurateMagic(magictype):
            return 2

        elif MagicCard.isSummonMagic(magictype):
            return 3

        elif MagicCard.isSpecialMagic(magictype):
            return 3 

        elif MagicCard.isConsumeMagic(magictype):
            return 0



class TreasureCard(Card):
    def __init__(self, name):
        Card.__init__(self, CardType.TREASURE, name)



#if __name__ == "__main__":
#    for i in list(map(int, MagicType)):
#        print("{:x} {} {} {:x} {}".format(i, MagicCard.getMagicName(i), MagicCard.getMagicLevel(i,0), MagicCard.getDemand(i), MagicCard.getDemandString(MagicCard.getDemand(i))))
#

