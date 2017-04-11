from MovesetFactory import *


class Watchmaker:
    @staticmethod
    def run():
        Dialgarithm.set_meta('xy', 'OU')
        DexFactory().get_dex()
        mf = MovesetFactory()
        mf.read_pokemon('Charizard')

Watchmaker.run()