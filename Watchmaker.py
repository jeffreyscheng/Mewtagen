from UsageReader import *
from Metagame import *
from MovesetFactory import *


class Watchmaker:
    @staticmethod
    def run():
        Dialgarithm.set_link('ou-1825.txt')
        DexFactory().get_dex()
        UsageReader.get_usage()
        MovesetFactory().get_movesets()
        Battle().get_all_counters()
        checks = {moveset.name: [x.name for x in Dialgarithm.counters_dict[moveset]] for moveset in Dialgarithm.moveset_list}
        print(len(checks['Tyranitar_Choice Scarf']))
        print(len(checks))
        # Metagame().precomputation()

        # next, test metagame generation with initial population + elos
        # each folder has xy_dex, xy_movesets, xy_damage_cache


Watchmaker.run()
