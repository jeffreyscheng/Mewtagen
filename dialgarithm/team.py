import random
from numpy.linalg import matrix_power
from .damage import *
from .model_local import *
from .Writer import *
import time


class SubTeam:
    def __init__(self, list_of_pokemon):
        self.members = list_of_pokemon

    def mutate(self):
        self.members = [mon.mutate() for mon in self.members]

    def __str__(self):
        return ', '.join([mon.name for mon in self.members])

    @staticmethod
    def crossover(sub1, sub2):
        length = len(sub1.members)
        point = random.randint(0, length - 1)
        new_members = sub1.members[0:point] + sub2.members[point:length]
        if len(new_members) != length:
            raise ValueError("chromosome length grew!")
        return SubTeam(new_members)


class Team:
    def __init__(self, core, suggestions):
        self.core = core
        self.suggestions = suggestions
        self.members = core.members + self.suggestions.members
        self.battler = {mon: 1 for mon in self.members}
        self.current = None
        # self.counter_matrix = None
        # self.transition_matrix = None
        # self.switch_costs = None
        # self.metrics = None

    @staticmethod
    def weighted_sample():

        dict_of_movesets_usage = \
            {m_set: m_set.usage for m_set in
             [mon for name, mon in Model.moveset_dict.items()]}
        total = sum([dict_of_movesets_usage[key] for key
                     in dict_of_movesets_usage])
        r = random.uniform(0, total)
        runner = 0
        for key, value in dict_of_movesets_usage.items():
            if runner + value >= r:
                return key
            runner += value
        assert False, "Shouldn't get here"

    def is_valid(self):
        list_of_names = [m_set.pokemon.dex_name for m_set in self.members]
        unique = len(list(set(list_of_names))) == 6
        no_ditto = 'Ditto' not in [mon.pokemon.dex_name for mon in self.members]
        return unique and no_ditto

    def is_fainted(self):
        return self.battler[self.current] == 0

    def still_playing(self):
        return len([health for mon, health
                    in self.battler.items() if health > 0]) > 0

    def heal(self):
        self.current = None
        self.battler = {mon: 1 for mon in self.members}

    def damage_current(self, damage):
        if np.isnan(damage):
            raise ValueError("NaN damage!")
        self.battler[self.current] -= damage
        if self.battler[self.current] < 0:
            self.battler[self.current] = 0

    def has_living_counter(self, opponent):
        return len([mon for mon, health
                    in self.battler.items() if mon
                    in Model.counters_dict[opponent] and
                    health > 0]) > 0

    def switch(self, opponent=None):
        if opponent is None:
            alive = [mon for mon, health in self.battler.items() if health > 0]
            self.current = random.choice(alive)
            return
        alive_counters = [mon for mon, health in self.battler.items() if
                          mon in Model.counters_dict[opponent] and
                          health > 0]
        if len(alive_counters) > 0:
            self.current = random.choice(alive_counters)
        else:
            alive = [mon for mon, health in self.battler.items() if health > 0]
            self.current = random.choice(alive)

    def get_elite(self):
        return Team(self.core, self.suggestions)

    @staticmethod
    def reproduce(team1, team2):
        # TODO: defensively check cores
        new_suggestions = SubTeam.crossover(team1.suggestions, team2.suggestions)
        new_suggestions.mutate()
        if len(team1.core.members) + len(new_suggestions.members) != 6:
            raise ValueError("Team with bad member count!")
        return Team(team1.core, new_suggestions)

    def __str__(self):
        return ', '.join([mon.name for mon in self.battler])

    # @staticmethod
    # def get_usage_sum(list_of_movesets):
    #     list_of_pokemon = list(set([mon.pokemon.unique_name for mon
    #                                 in list_of_movesets]))
    #     ans = sum([Model.usage_dict[mon] for mon in
    #                [mon for mon in list_of_pokemon if mon in Model.usage_dict]])
    #     if ans > 1:
    #         raise ValueError("usage greater than 1")
    #     return ans
    #
    # def analyze(self):
    #     tick = time.clock()
    #     arr = np.zeros((6, 6))
    #     self.metrics = \
    #         pd.DataFrame(data=arr, index=self.team_names,
    #                      columns=['teammate', 'ssp', 'dpt_taken',
    #                               'turns_lasted', 'dpt_given', 'total_damage'])
    #     self.metrics['teammate'] = self.team_names
    #     self.set_counters()
    #     self.set_ssp()
    #     self.set_switch_costs()
    #     self.set_damage_taken()
    #     self.set_turns_lasted()
    #     self.set_damage_given()
    #     self.set_total_damage()
    #     elapsed = time.clock() - tick
    #     print("TEAM ANALYZED IN: " + str(elapsed) + " seconds.")
    #
    # def set_counters(self):
    #     arr = np.zeros((6, 6))
    #     self.counter_matrix = \
    #         pd.DataFrame(data=arr, index=self.team_names,
    #                      columns=self.team_names)
    #     self.counter_matrix = self.counter_matrix.astype('object')
    #     for row in self.team_names:
    #         row_moveset = Model.moveset_dict[row]
    #         for column in self.team_names:
    #             column_moveset = Model.moveset_dict[column]
    #             self.counter_matrix.loc[row, column] = \
    #                 [mon for mon in Model.counters_dict[row_moveset]
    #                  if mon not in Model.counters_dict[column_moveset]]
    #
    # def set_ssp(self):
    #     arr = np.zeros((6, 6))
    #     if len(self.team_names) < 6:
    #         print(self.team_names)
    #         print(self.battler)
    #         raise ValueError("Fewer than 6 team members!")
    #     transition_mat = \
    #         pd.DataFrame(data=arr, index=self.team_names,
    #                      columns=self.team_names)
    #     for row in self.team_names:
    #         row_moveset = Model.moveset_dict[row]
    #         d = Model.counters_dict
    #         self_loop = 1 - self.get_usage_sum(d[row_moveset])
    #         for column in self.team_names:
    #             if row == column:
    #                 transition_mat.loc[row, column] = self_loop
    #             else:
    #                 transition_mat.loc[row, column] = \
    #                     self.get_usage_sum(self.counter_matrix.loc[row,
    #                                                                column])
    #         if sum(transition_mat.loc[row, :]) - self_loop == 0:
    #             print(row)
    #             raise ValueError("Divide by zero!")
    #         normalization_factor = (1 - self_loop) / \
    #                                (sum(transition_mat.loc[row, :]) -
    #                                 self_loop)
    #         for column in self.team_names:
    #             if row != column:
    #                 transition_mat.loc[row, column] *= normalization_factor
    #
    #     self.transition_matrix = transition_mat
    #     stationary = matrix_power(transition_mat, 100)
    #     stationary = stationary[0]
    #     self.metrics.loc[:, 'ssp'] = stationary
    #
    # def set_switch_costs(self):
    #     arr = np.zeros((6, 6))
    #     self.switch_costs = \
    #         pd.DataFrame(data=arr, index=self.team_names,
    #                      columns=self.team_names)
    #     for row in self.team_names:
    #         row_moveset = Model.moveset_dict[row]
    #         for column in self.team_names:
    #             column_moveset = Model.moveset_dict[column]
    #             self.switch_costs.loc[row, column] = \
    #                 Damage.get_weighted_switch_damage(row_moveset,
    #                                                   column_moveset)
    #
    # def set_damage_taken(self):
    #     def get_damage_taken(mon):
    #         damages = [(self.switch_costs.loc[mon2, mon],
    #                     self.metrics.loc[mon2, 'ssp'],
    #                     self.transition_matrix.loc[mon2, mon])
    #                    for mon2 in self.team_names]
    #         return sum([a * b * c for a, b, c in damages] /
    #                    self.metrics.loc[mon, 'ssp'])
    #
    #     self.metrics['dpt_taken'] = \
    #         self.metrics['teammate'].map(lambda x: get_damage_taken(x))
    #     # print(self.metrics['dpt_taken'])
    #
    # def set_turns_lasted(self):
    #     def get_turns_lasted(mon):
    #         return 1 / self.metrics.loc[mon, 'dpt_taken']
    #
    #     self.metrics['turns_lasted'] = \
    #         self.metrics['teammate'].map(get_turns_lasted)
    #
    # def set_damage_given(self):
    #     self.metrics['dpt_given'] = \
    #         self.metrics['teammate'].map(Damage.get_weighted_attack_damage)
    #
    # def set_total_damage(self):
    #     def get_total_damage(row):
    #         return row['turns_lasted'] * row['dpt_given']
    #
    #     self.metrics['total_damage'] = \
    #         self.metrics.apply(get_total_damage, axis=1)
    #

    # def display(self):
    #     print('==========')
    #     for mon in self.members:
    #         print('OOOOO')
    #         print('Name: ' + mon.name)
    #         print('Expected Turns Lasted: ' +
    #               str(self.metrics.loc[mon.name, 'turns_lasted']))
    #         print('Expected Damage Output ' +
    #               str(self.metrics.loc[mon.name, 'total_damage']))
    #     print('==========')
