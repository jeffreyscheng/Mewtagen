from MovesetFactory import *


class Watchmaker:
    @staticmethod
    def run():
        Dialgarithm.set_meta('xy', 'OU')
        DexFactory().get_dex()
        MovesetFactory().read_all_movesets()

Watchmaker.run()
