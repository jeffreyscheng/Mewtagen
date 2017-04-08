import random
import time
from Team import Team
from Battle import Battle
from MovesetFactory import MovesetFactory


class Metagame:
    def __init__(self, dex, meta_format):
        self.dex = dex
        self.format = meta_format
        self.dict_of_movesets_usage = self.get_movesets_list()
        self.dict_of_team_elo = {}
        self.beta_offense = 0
        self.beta_defense = 0

    def get_movesets_list(self):
        return MovesetFactory(self.dex, self.format).read_all_movesets()

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
        attempt = [weighted_sample(self.dict_of_movesets_usage) for i in range(0, num_teammates)]
        new_team = Team(attempt)
        if new_team.is_valid():
            return new_team
        else:
            return self.generate_team(core)  # this can be optimized

    def precomputation(self):
        """generates teams, battles them over 24 hours, gets regression from expectations -> Elo"""
        self.dict_of_team_elo = {self.generate_team() for i in
                                 range(0, 1000)}  # teams should be 2.4 hr / (time per game)
        tick = time.clock()
        while time.clock() - tick < 24 * 3600:
            # sort by elo
            bracket = sorted(self.dict_of_team_elo, key=self.dict_of_team_elo.get)
            # pair off and battle down the line
            for i in range(0, 500):
                team1 = bracket[2 * i]
                team2 = bracket[2 * i + 1]
                self.run_battle(team1, team2)
        # pandas df with Team / Elo / Expected Damage Output / Expected Damage Input

    # TODO
    def run_battle(self, team1, team2):
        # determine winner
        winner = Battle.battle(team1, team2)
        if winner is team1:
            loser = team2
        else:
            loser = team1
        # update elos
        self.dict_of_team_elo[winner] = 1000  # do
        self.dict_of_team_elo[loser] = 1000  # do
