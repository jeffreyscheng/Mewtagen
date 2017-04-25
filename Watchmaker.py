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
        Damage.read_damage_cache()
        Damage.get_all_counters()
        Damage.get_switches()
        # Metagame().precomputation()

        tick = time.clock()
        for i in range(0, 100):
            t = Metagame().generate_team()
            t.analyze()
        tock = time.clock()
        print(tock - tick)

        # next, test metagame generation with initial population + elos
        # each folder has xy_dex, xy_movesets, xy_damage_cache


Watchmaker.run()
