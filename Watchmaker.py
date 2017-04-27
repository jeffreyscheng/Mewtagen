from UsageReader import *
from MovesetFactory import *
from Metagame import *
import random


class Watchmaker:
    @staticmethod
    def run():
        Dialgarithm.set_link('ou-1825.txt')
        DexFactory().get_dex()
        UsageReader.get_usage()
        MovesetFactory().get_movesets()

        core_size = int(input("How big is your core? (0-5) \n"))
        if core_size < 0 or core_size > 5:
            raise ValueError("Bad core size!")
        for i in range(1, core_size + 1):
            flag = True
            while flag:
                name = input("Name of Pokemon " + str(i) + "?\n")
                potential_movesets = [mon for mon in Dialgarithm.moveset_list
                                      if mon.pokemon.unique_name == name]
                if len(potential_movesets) > 0:
                    Dialgarithm.core.append(random.choice(potential_movesets))
                    flag = False
                else:
                    print("Pick a better Pokemon!")
        Dialgarithm.population_size = int(input("Population size? (>3) \n"))
        Dialgarithm.time = int(input("Evolution duration?\n"))
        print("Inputs processed!")

        Damage.start()
        Metagame().precomputation()
        Damage.end()

Watchmaker.run()
