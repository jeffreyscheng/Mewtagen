from .metagame import *
import numpy as np
import math

class Evolve:
    population_size = 5
    num_generations = 5
    population = []
    fitness_dict = {}
    starting_elo = 1000
    matches = 10

    @staticmethod
    def evolve():
        tick = time.clock()
        print("GENERATING TEAMS!")
        Evolve.population = [Metagame.generate_team(Model.core) for _ in range(0, Evolve.population_size)]
        for generation in range(0, Evolve.num_generations):
            Evolve.next_generation()
        print(Evolve.population)
        Evolve.final_evaluation()
        print(time.clock() - tick)

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
                elo = Elo.update_elo(elo, norm_elo, winner)
            return Elo.win_prob(elo)

        tick = time.clock()
        Evolve.fitness_dict = {team: fitness(team) for team in Evolve.population}
        tock = time.clock()
        print(len(norms) * Evolve.population_size, "battles completed in:", tock - tick, "seconds.")

        # damage - 1800, switch - 1000

        choices = [key for key in Evolve.fitness_dict]
        weights = [Evolve.fitness_dict[key] for key in Evolve.fitness_dict]
        total_weight = sum(weights)
        weights = [weight / total_weight for weight in weights]

        def get_newborn():
            parents = np.random.choice(choices, 2, p=weights)
            return Team.reproduce(parents[0], parents[1])

        elites = Evolve.get_elites()
        mutants = [get_newborn() for _ in range(0, Evolve.population_size - len(elites))]
        Evolve.population = elites + mutants

    @staticmethod
    def get_elites():
        elites = sorted(Evolve.fitness_dict,
                        key=Evolve.fitness_dict.get,
                        reverse=True)[:math.floor(Evolve.population_size / 10)]
        return [team.get_elite() for team in elites]

    @staticmethod
    def final_evaluation():
        # grab |matches| sample of norms
        norm_choices = [key for key in Metagame.elo_dict]
        norms = np.random.choice(norm_choices, Evolve.matches)

        # battles all norms against team, returns elo
        def precise_fitness(team):
            elo = Evolve.starting_elo
            for i in range(0, 50):
                for norm in norms:
                    winner = Damage.battle(team, norm)
                    norm_elo = Metagame.elo_dict[norm]
                    elo = Elo.update_elo(elo, norm_elo, winner)
            return elo
        Evolve.fitness_dict = {team: precise_fitness(team) for team in Evolve.population}
        elites = sorted(Evolve.fitness_dict, key=Evolve.fitness_dict.get)[:10]
        for team in elites:
            print(team, Evolve.fitness_dict[team])