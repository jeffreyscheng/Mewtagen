import random
import Team

class Metagame:
    def __init__(self, dex, movesets_set, format):
        self.dex = dex
        self.dict_of_movesets_usage = movesets_set
        self.dict_of_team_elo = {}
        self.beta_offense = 0
        self.beta_defense = 0

    @staticmethod
    def weighted_sample(population):
        total = sum([population[key] for key in population])
        r = random.uniform(0, total)
        runner = 0
        for key, value in population.items():
            if runner + value >= r:
                return key
            runner += value
        assert False, "Shouldn't get here"

    def generate_team(self, core=None):
        if core is None:
            num_teammates = 6
        else:
            num_teammates = 6 - len(core)
        attempt = []
        for i in range(0, num_teammates):
            attempt.append(self.weighted_sample(self.dict_of_movesets_usage))
        new_team = Team(attempt)
        if new_team.is_valid():
            return new_team
        else:
            return self.generate_team(core)


    def precomputation(self):
        """generates teams, battles them over 24 hours, gets regression from expectations -> Elo"""
        self.dict_of_team_elo = {team:0 for team in []}    # teams should be 2.4 hr / (time per game)
