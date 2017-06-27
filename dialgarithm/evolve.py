from .metagame import *
import numpy as np


class Evolve:
    population_size = 10
    num_generations = 10
    population = []
    starting_elo = 1000
    matches = 50

    @staticmethod
    def evolve():
        print("GENERATING TEAMS!")
        Evolve.population = [Metagame.generate_team(Model.core) for _ in range(0, Evolve.population_size)]
        for generation in range(0, Evolve.num_generations):
            Evolve.next_generation()
        print(Evolve.population)

    @staticmethod
    def next_generation():

        # grab |matches| sample of norms
        norm_choices = [key for key in Metagame.elo_dict]
        norms = np.random.choice(norm_choices, Evolve.matches)

        # battles all norms against team, returns elo
        def fitness(team):
            elo = Evolve.starting_elo
            for norm in norms:
                winner = Damage.battle(team, norm)
                norm_elo = Metagame.elo_dict[norm]
                team1_winner = winner == team
                elo = Elo.update_elo(elo, norm_elo, team1_winner)
            return Elo.win_prob(elo)

        fitness_dict = {team: fitness(team) for team in Evolve.population}

        # damage - 1800, switch - 1000

        choices = [key for key in fitness_dict]
        weights = [fitness_dict[key] for key in fitness_dict]
        total_weight = sum(weights)
        weights = [weight / total_weight for weight in weights]

        def get_newborn():
            parents = np.random.choice(choices, 2, p=weights)
            return parents[0].reproduce(parents[1])

        Evolve.population = [get_newborn() for _ in range(0, Evolve.population_size)]
