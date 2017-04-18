from UsageReader import *
from Metagame import *


class Watchmaker:
    @staticmethod
    def run():
        Dialgarithm.set_link('ou-1825.txt')
        DexFactory().get_dex()
        UsageReader.get_usage()
        MovesetFactory().get_movesets()
        print(Metagame().generate_team())

        # next, test metagame generation with initial population + elos
        # each folder has xy_dex, xy_movesets, xy_damage_cache


Watchmaker.run()
