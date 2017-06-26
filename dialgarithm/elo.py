# temp script to ascertain whether elo separation really exists
# success: if std > 200

from .team import *
from .model_local import *
import random
from functools import wraps


class Elo:
    def __init__(self):
        self.dex = Model.gen
        self.format = Model.format
        self.dict_of_team_elo = {}
        self.beta_offense = 0
        self.beta_defense = 0

    def generate_team(self, core=[]):
        num_teammates = 6 - len(core)
        attempt = [Team.weighted_sample() for i in range(0, num_teammates)]
        attempt += core
        new_team = Team(attempt)
        if new_team.is_valid():
            if len(list(set([mon.pokemon.dex_name for mon in attempt]))) < 6:
                print([mon.pokemon.dex_name for mon in attempt])
                raise ValueError("Not a valid team!")
            return new_team
        else:
            return self.generate_team(core)  # this can be optimized

    def precomputation(self):
        """generates teams, battles them over 24 hours,
        gets regression from expectations -> Elo"""
        print("GENERATING TEAMS!")
        number_of_teams = 100000  # change to 100,000
        starting_elo = 1000
        self.dict_of_team_elo = \
            {self.generate_team([]): (starting_elo, 0, 0) for i
             in range(0, number_of_teams)}
        tick = time.clock()
        seconds_spent = 3600 * 24 * 7
        counter = 0

        # damage - 1800, switch - 1000

        # each cycle takes roughly 15 seconds
        print("BEGINNING CYCLES")
        while time.clock() - tick < seconds_spent:
            for i in range(0, 30):
                counter += 1
                # sort by elo
                bracket = sorted(self.dict_of_team_elo, key=self.dict_of_team_elo.get)
                if random.random() > 0.9:
                    random.shuffle(bracket)
                # pair off and battle down the line
                for i in range(0, number_of_teams // 2):
                    team1 = bracket[2 * i]
                    team2 = bracket[2 * i + 1]
                    self.run_battle(team1, team2)
        print(self.dict_of_team_elo)

    @staticmethod
    def compute_expected(elo1, elo2):
        return 1 / (1 + 10.0 ** ((elo2 - elo1) / 400.0))

    # TODO
    def run_battle(self, team1, team2):
        elo1 = self.dict_of_team_elo[team1][0]
        elo2 = self.dict_of_team_elo[team2][0]
        expected_1 = Elo.compute_expected(elo1, elo2)
        expected_2 = Elo.compute_expected(elo2, elo1)
        # determine winner
        winner = Damage.battle(team1, team2)
        k = 16
        if winner is team1:
            team1_elo = elo1 + k * (1 - expected_1)
            team1_wins = self.dict_of_team_elo[team1][1] + 1
            team1_losses = self.dict_of_team_elo[team1][2]
            self.dict_of_team_elo[team1] = (team1_elo, team1_wins, team1_losses)
            team2_elo = elo2 + k * (0 - expected_2)
            team2_wins = self.dict_of_team_elo[team2][1]
            team2_losses = self.dict_of_team_elo[team2][2]+1
            self.dict_of_team_elo[team2] = (team2_elo, team2_wins, team2_losses)
        else:
            team1_elo = elo1 + k * (0 - expected_1)
            team1_wins = self.dict_of_team_elo[team1][1]
            team1_losses = self.dict_of_team_elo[team1][2] + 1
            self.dict_of_team_elo[team1] = (team1_elo, team1_wins, team1_losses)
            team2_elo = elo2 + k * (1 - expected_2)
            team2_wins = self.dict_of_team_elo[team2][1]
            team2_losses = self.dict_of_team_elo[team2][2]+1
            self.dict_of_team_elo[team2] = (team2_elo, team2_wins, team2_losses)
