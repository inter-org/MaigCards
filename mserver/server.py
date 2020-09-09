from general.gameinfo import *


class Server:

    @staticmethod
    def unserialize(bytes_):
        typ = PacketType(int.from_bytes(bytes_[0:1], byteorder='big'))
        performer = (int.from_bytes(bytes_[1:2], byteorder='big'))
        game_id = (int.from_bytes(bytes_[2:4], byteorder='big'))

        if typ == PacketType.PICK:
            card_type = CardType(int.from_bytes(bytes_[4:5], byteorder='big'))
            return "{}: {} picks {}".format(game_id, performer, ["Gem", "Magic", "Treasure"][card_type - 1])

        if typ == PacketType.ACT:
            target = int.from_bytes(bytes_[4:5], byteorder='big')

        if typ == PacketType.ACT or typ == PacketType.DROP:
            num_of_cards = int.from_bytes((bytes_[5:7]) if typ == PacketType.ACT else (bytes_[4:6]), byteorder='big')
            cards = []

            index = 8 if typ == PacketType.ACT else 7
            for i in range(0, num_of_cards):
                cards.append(int.from_bytes(bytes_[index:index + 2], byteorder='big'))
                index = index + 3

            names = [MagicCard.getMagicName(x) for x in cards]
            if typ == PacketType.ACT:
                return "{}: {} uses {} to atk {}".format(game_id, performer, " ".join(names), target)
            else:
                return "{}: {} drops {}".format(game_id, performer, " ".join(names))

        if typ == PacketType.SKIP:
            return "{}: {} finished his/her round".format(game_id, performer)

        if typ == PacketType.THROW:
            return "{}: {} throw the dice".format(game_id, performer)
