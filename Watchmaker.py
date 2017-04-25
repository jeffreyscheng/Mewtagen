from UsageReader import *
from MovesetFactory import *
from Metagame import *
import time


class Watchmaker:
    @staticmethod
    def run():
        Dialgarithm.set_link('ou-1825.txt')
        DexFactory().get_dex()
        UsageReader.get_usage()
        MovesetFactory().get_movesets()
        Damage.start()
        tick = time.clock()
        print('PRECOMPUTING')
        Metagame().precomputation()
        tock = time.clock()
        print(tock - tick)

        Damage.end()

        # next, test metagame generation with initial population + elos
        # each folder has xy_dex, xy_movesets, xy_damage_cache


Watchmaker.run()
