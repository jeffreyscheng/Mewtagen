from UsageReader import *
from MovesetFactory import *
from Metagame import *


class Watchmaker:
    @staticmethod
    def run():
        Dialgarithm.set_link('ou-1825.txt')
        DexFactory().get_dex()
        UsageReader.get_usage()
        MovesetFactory().get_movesets()
        Damage.get_all_counters()
        Damage.get_switches()
        chansey = Dialgarithm.moveset_dict['Infernape_Physically Defensive']
        print(len(Dialgarithm.counters_dict[chansey]))
        print(len(Dialgarithm.counters_dict.keys()))
        # Metagame().precomputation()
        for i in range(0, 100):
            t = Metagame().generate_team()
            t.analyze()

        # next, test metagame generation with initial population + elos
        # each folder has xy_dex, xy_movesets, xy_damage_cache


Watchmaker.run()
