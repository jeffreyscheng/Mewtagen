import math
import numpy as np
import pandas as pd
import random
from Dialgarithm import *


class Team:
    def __init__(self, list_of_movesets):
        self.party = {moveset: 1 for moveset in list_of_movesets}
        self.current = None
        self.ssp = {moveset: 1 / 6 for moveset in list_of_movesets}
        self.turns_lasted = {moveset: 5 for moveset in list_of_movesets}
        self.damage_output = {moveset: 0 for moveset in list_of_movesets}

    def is_valid(self):
        list_of_names = [m_set.pokemon.dex_name for m_set in self.party.keys()]
        return np.unique(list_of_names).size == 6

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

    def set_ssp(self):

        team_names = [mon.name for mon in self.party.keys()]

        arr = np.zeros((6, 6))
        transition_mat = pd.DataFrame(data=arr, index=team_names, columns=team_names)
        for row in team_names:
            row_moveset = Dialgarithm.moveset_dict[row]
            self_loop = 1 - self.get_usage_sum(Dialgarithm.counters_dict[row_moveset])
            for column in team_names:
                column_moveset = Dialgarithm.moveset_dict[column]
                if row == column:
                    transition_mat.loc[row, column] = self_loop
                else:
                    counters_column_not_row = [mon for mon in Dialgarithm.counters_dict[column_moveset]
                                               if mon not in Dialgarithm.counters_dict[row_moveset]]
                    transition_mat.loc[row, column] = self.get_usage_sum(counters_column_not_row)
            normalization_factor = (1 - self_loop) / (sum(transition_mat.loc[row, :]) - self_loop)
            print(self_loop + (sum(transition_mat.loc[row, :]) - self_loop) * normalization_factor)
            for column in team_names:
                if row != column:
                    transition_mat.loc[row, column] *= normalization_factor

        for row in team_names:
            print(sum(transition_mat.loc[row, :]))
            if math.isnan(sum(transition_mat.loc[row, :])):
                print([mon.name for mon in self.party.keys()])
                raise ValueError

                # transition matrix = M
                # transition_mat = np.matrix([
                #     [.9, .075, 0.025],
                #     [0.15, 0.8, 0.05],
                #     [0.25, 0.25, 0.5]])
                # eigenvalues, eigenvectors = eig(transition_mat, right=False, left=True)
                # stationary = np.array(eigenvectors[:, np.where(np.abs(eigenvalues - 1.) < 1e-8)[0][0]].flat)
                # stationary = stationary / np.sum(stationary)
                # print(stationary)








                # for row in damage_graph.index:
                #     num_counters = len(self.counters[row])
                #     counter_sum = 0
                #     for col in damage_graph.columns:
                #         a, b = self.get_switch_costs(row, col)
                #         damage_graph.loc[row, col] = b
                #         probability_graph.loc[row, col] = a
                #         counter_sum += a
                #     for col in probability_graph.columns:
                #         if row != col:
                #             card = probability_graph.loc[row, col]
                #             probability_graph.loc[row, col] = card / counter_sum * num_counters / num_sets
                #         if row == col:
                #             probability_graph.loc[row, col] = 1 - num_counters / num_sets
                # steady_state = probability_graph
                # for i in range(10):
                #     steady_state = steady_state.dot(probability_graph)
