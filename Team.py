import numpy as np
import random
from Dialgarithm import *


class Team:
    def __init__(self, list_of_movesets):
        self.party = {moveset: 1 for moveset in list_of_movesets}
        self.current = None

    def is_valid(self):
        list_of_names = [m_set.pokemon.dex_name for m_set in self.party.keys()]
        return np.unique(list_of_names).size == len(list_of_names)

    def is_fainted(self):
        return self.party[self.current] == 0

    def is_blacked_out(self):
        return len([health for mon, health in self.party if health > 0]) > 0

    def heal(self):
        self.party = {moveset: 1 for moveset in self.party.keys()}
        self.current = None

    def damage_current(self, damage):
        self.party[self.current] -= damage
        if self.party[self.current] < 0:
            self.party[self.current] = 0

    def switch(self, opponent):
        alive_counters = [mon for mon, health in self.party.items() if mon in Dialgarithm.counters_dict[opponent] and health > 0]
        if len(alive_counters) > 0:
            self.current = random.choice(alive_counters)
        else:
            alive = [mon for mon, health in self.party.items() if health > 0]
            self.current = random.choice(alive)

