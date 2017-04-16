from MovesetFactory import *
from UsageReader import *


class Watchmaker:
    @staticmethod
    def run():
        Dialgarithm.set_link('ou-1825.txt')
        DexFactory().get_dex()
        UsageReader.get_usage()
        MovesetFactory().get_movesets()
        # print(len(Dialgarithm.moveset_dict))

        # first, work on pulling usage stats
        # next, test metagame generation with initial population + elos
        # each folder has xy_dex, xy_movesets, xy_damage_cache


Watchmaker.run()
