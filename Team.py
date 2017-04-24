import math
import numpy as np
import pandas as pd
import random
from numpy.linalg import matrix_power
from Damage import *


class Team:
    def __init__(self, list_of_movesets):
        self.party = {moveset: 1 for moveset in list_of_movesets}
        self.current = None
        self.transition_matrix = None
        self.ssp = None
        self.switch_costs = None

    def is_valid(self):
        list_of_names = [m_set.pokemon.dex_name for m_set in self.party.keys()]
        unique = len(list(set(list_of_names))) == 6
        no_ditto = 'Ditto' not in [mon.pokemon.dex_name for mon in self.party.keys()]
        return unique and no_ditto

    def is_fainted(self):
        return self.party[self.current] == 0

    def still_playing(self):
        return len([health for mon, health in self.party.items() if health > 0]) > 0

    def heal(self):
        self.party = {moveset: 1 for moveset in list(self.party.keys())}
        self.current = None

    def damage_current(self, damage):
        self.party[self.current] -= damage
        if self.party[self.current] < 0:
            self.party[self.current] = 0

    def has_living_counter(self, opponent):
        return len([mon for mon, health in self.party.items() if
                    mon in Dialgarithm.counters_dict[opponent] and health > 0]) > 0

    def switch(self, opponent=None):
        if opponent is None:
            alive = [mon for mon, health in self.party.items() if health > 0]
            self.current = random.choice(alive)
            return
        alive_counters = [mon for mon, health in self.party.items() if
                          mon in Dialgarithm.counters_dict[opponent] and health > 0]
        if len(alive_counters) > 0:
            self.current = random.choice(alive_counters)
        else:
            alive = [mon for mon, health in self.party.items() if health > 0]
            self.current = random.choice(alive)

    def __str__(self):
        return ', '.join([mon.name for mon in self.party])

    @staticmethod
    def get_usage_sum(list_of_movesets):
        list_of_pokemon = list(set([mon.pokemon.unique_name for mon in list_of_movesets]))
        ans = sum([Dialgarithm.usage_dict[mon] for mon in list_of_pokemon])
        if ans > 1:
            raise ValueError("usage greater than 1")
        return ans

    @staticmethod
    def get_weighted_switch_damage(bailer, victim):
        contributions = [Dialgarithm.usage_dict[mon] * Damage.deal_damage()]

    def analyze(self):
        self.set_ssp()
        self.set_switch_costs()

    def set_ssp(self):

        team_names = [mon.name for mon in self.party.keys()]

        arr = np.zeros((6, 6))
        if len(team_names) < 6:
            print(team_names)
            print(self.party)
            raise ValueError("Fewer than 6 team members!")
        transition_mat = pd.DataFrame(data=arr, index=team_names, columns=team_names)
        for row in team_names:
            row_moveset = Dialgarithm.moveset_dict[row]
            self_loop = 1 - self.get_usage_sum(Dialgarithm.counters_dict[row_moveset])
            for column in team_names:
                column_moveset = Dialgarithm.moveset_dict[column]
                if row == column:
                    transition_mat.loc[row, column] = self_loop
                else:
                    counters_row_not_column = [mon for mon in Dialgarithm.counters_dict[row_moveset]
                                               if mon not in Dialgarithm.counters_dict[column_moveset]]
                    transition_mat.loc[row, column] = self.get_usage_sum(counters_row_not_column)
            if sum(transition_mat.loc[row, :]) - self_loop == 0:
                print(row)
                raise ValueError("Divide by zero!")
            normalization_factor = (1 - self_loop) / (sum(transition_mat.loc[row, :]) - self_loop)
            for column in team_names:
                if row != column:
                    transition_mat.loc[row, column] *= normalization_factor

        self.transition_matrix = transition_mat
        stationary = matrix_power(transition_mat, 100)
        stationary = stationary[0]
        df = pd.DataFrame(data=stationary, index=team_names)
        self.ssp = df.transpose().to_dict(orient='list')
        self.ssp = {key: value[0] for key, value in self.ssp.items()}
        print(self.ssp)

    def set_switch_costs(self):
        team_names = [mon.name for mon in self.party.keys()]
        arr = np.zeros((6, 6))
        switch_matrix = pd.DataFrame(data=arr, index=team_names, columns=team_names)
        for row in team_names:
            for column in team_names:
                if row == column:
                    pass