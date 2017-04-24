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
        b = Battle()
        b.get_all_counters()
        # Metagame().precomputation()
        for i in range(0,100):
            t = Metagame().generate_team()
            t.set_ssp()

        #['Ditto_Imposter', 'Jolteon_All-Out Attacking', 'Rotom-Wash_Physically Defensive Pivot', 'Hydreigon_Choice Scarf', 'Keldeo_Choice Scarf', 'Talonflame_Revenge Killer']
        # ['Venusaur_Sun Sweeper', 'Ditto_Imposter', 'Medicham_Life Orb', 'Jirachi_Specially Defensive', 'Rotom-Wash_Physically Defensive Pivot', 'Sceptile_Life Orb']
        #    ['Shuckle_Holy Shuck!', 'Mew_Stallbreaker', 'Diancie_Defensive', 'Lopunny_Offensive Utility', 'Excadrill_Sand Rush Sweeper', 'Medicham_Life Orb']

        # next, test metagame generation with initial population + elos
        # each folder has xy_dex, xy_movesets, xy_damage_cache


Watchmaker.run()
