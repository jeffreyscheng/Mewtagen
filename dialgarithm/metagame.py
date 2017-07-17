from .team import *
from .damage import *
from .model_local import *


class Metagame:
    elo_start = 1000
    k = 32
    # generation = 0
    # crossover = 0.8
    # elitism = 0.1
    # mutation_rate = 0.01

    elo_dict = {}

    @staticmethod
    def generate_team(core=[]):
        num_teammates = 6 - len(core)
        attempt = [Team.weighted_sample() for _ in range(0, num_teammates)]

        def generate_core():
            return [np.random.choice(Model.core[i]) for i in range(0, len(Model.core))]

        new_team = Team(Core(generate_core()), Suggestion(attempt))
        if new_team.is_valid():
            if len(list(set([mon.pokemon.dex_name for mon in attempt]))) + len(core) < 6:
                print([mon.pokemon.dex_name for mon in attempt])
                raise ValueError("Not a valid team!")
            return new_team
        else:
            return Metagame.generate_team(core)

    @staticmethod
    def generate_norms():
        tentative_norms = Writer.load_pickled_object('norms.txt')
        if tentative_norms is None:
            number_of_norms = 1000
            Model.elo_dict = {Metagame.generate_team(): Metagame.elo_start for _ in range(number_of_norms)}
            for i in range(0, 100):
                bracket = sorted(Model.elo_dict, key=Model.elo_dict.get)
                if i % 10 == 0:
                    random.shuffle(bracket)
                # pair off and battle down the line
                for j in range(0, number_of_norms // 2):
                    team1 = bracket[2 * j]
                    team2 = bracket[2 * j + 1]
                    Metagame.run_battle(team1, team2)
            Writer.save_pickled_object(Model.elo_dict, 'norms.txt')
        else:
            Model.elo_dict = tentative_norms

    @staticmethod
    def run_battle(team1, team2):
        winner = Damage.battle(team1, team2)
        elo1 = Model.elo_dict[team1]
        elo2 = Model.elo_dict[team2]
        team1_winner = winner == team1
        Model.elo_dict[team1] = Elo.update_elo(elo1, elo2, team1_winner)
        Model.elo_dict[team2] = Elo.update_elo(elo2, elo1, not team1_winner)


class Elo:
    @staticmethod
    def compute_expected(elo1, elo2):
        return 1 / (1 + 10.0 ** ((elo2 - elo1) / 400.0))

    @staticmethod
    def win_prob(elo1):
        return 1 / (1 + 10.0 ** ((1000 - elo1) / 400.0))

    @staticmethod
    def update_elo(elo1, elo2, win):
        if win:
            result = 1
        else:
            result = 0
        return elo1 + Metagame.k * (result - Elo.compute_expected(elo1, elo2))
