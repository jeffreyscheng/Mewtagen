import random
from numpy.linalg import matrix_power
from Damage import *


class Team:

    mutate_prob = 0.05

    def __init__(self, list_of_movesets):
        self.party = {moveset: 1 for moveset in list_of_movesets}
        self.team_names = [mon.name for mon in self.party.keys()]
        self.current = None
        self.counter_matrix = None
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
        if np.isnan(damage):
            raise ValueError("NaN damage!")
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

    def analyze(self):
        self.set_counters()
        self.set_ssp()
        self.set_switch_costs()

    def set_counters(self):
        arr = np.zeros((6, 6))
        self.counter_matrix = pd.DataFrame(data=arr, index=self.team_names, columns=self.team_names)
        self.counter_matrix = self.counter_matrix.astype('object')
        for row in self.team_names:
            row_moveset = Dialgarithm.moveset_dict[row]
            for column in self.team_names:
                column_moveset = Dialgarithm.moveset_dict[column]
                self.counter_matrix.loc[row, column] = [mon for mon in Dialgarithm.counters_dict[row_moveset]
                                                        if mon not in Dialgarithm.counters_dict[column_moveset]]

    def set_ssp(self):
        arr = np.zeros((6, 6))
        if len(self.team_names) < 6:
            print(self.team_names)
            print(self.party)
            raise ValueError("Fewer than 6 team members!")
        transition_mat = pd.DataFrame(data=arr, index=self.team_names, columns=self.team_names)
        for row in self.team_names:
            row_moveset = Dialgarithm.moveset_dict[row]
            self_loop = 1 - self.get_usage_sum(Dialgarithm.counters_dict[row_moveset])
            for column in self.team_names:
                if row == column:
                    transition_mat.loc[row, column] = self_loop
                else:
                    transition_mat.loc[row, column] = self.get_usage_sum(self.counter_matrix.loc[row, column])
            if sum(transition_mat.loc[row, :]) - self_loop == 0:
                print(row)
                raise ValueError("Divide by zero!")
            normalization_factor = (1 - self_loop) / (sum(transition_mat.loc[row, :]) - self_loop)
            for column in self.team_names:
                if row != column:
                    transition_mat.loc[row, column] *= normalization_factor

        self.transition_matrix = transition_mat
        stationary = matrix_power(transition_mat, 100)
        stationary = stationary[0]
        df = pd.DataFrame(data=stationary, index=self.team_names)
        self.ssp = df.transpose().to_dict(orient='list')
        self.ssp = {key: value[0] for key, value in self.ssp.items()}

    def set_switch_costs(self):
        arr = np.zeros((6, 6))
        switch_matrix = pd.DataFrame(data=arr, index=self.team_names, columns=self.team_names)
        for row in self.team_names:
            row_moveset = Dialgarithm.moveset_dict[row]
            for column in self.team_names:
                column_moveset = Dialgarithm.moveset_dict[column]
                switch_matrix.loc[row, column] = Damage.get_weighted_switch_damage(row_moveset, column_moveset)

    @staticmethod
    def get_expected_damage(team):
        return 0

    @staticmethod
    def get_expected_turns_lasted(team):
        return 0

    @staticmethod
    def weighted_sample():
        dict_of_movesets_usage =\
            {m_set: m_set.usage for m_set in [mon for name, mon in Dialgarithm.moveset_dict.items()]}
        total = sum([dict_of_movesets_usage[key] for key in dict_of_movesets_usage])
        r = random.uniform(0, total)
        runner = 0
        for key, value in dict_of_movesets_usage.items():
            if runner + value >= r:
                return key
            runner += value
        assert False, "Shouldn't get here"

    def reproduce(self):
        def mutate(pokemon):
            if pokemon in Dialgarithm.core:
                return pokemon
            elif random.random() < Team.mutate_prob:
                return Team.weighted_sample()
            else:
                return pokemon
        candidate = Team([mutate(mon) for mon in self.party.keys()])
        if candidate.is_valid():
            return candidate
        else:
            return self.reproduce()


