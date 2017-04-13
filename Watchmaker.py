from MovesetFactory import *


class Watchmaker:
    @staticmethod
    def run():
        Dialgarithm.set_meta('xy', 'OU')
        DexFactory().get_dex()
        MovesetFactory().get_movesets()
        print(len(Dialgarithm.moveset_dict))

Watchmaker.run()
