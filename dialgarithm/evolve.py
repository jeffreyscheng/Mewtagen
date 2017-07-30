from .metagame import *
import numpy as np
import pandas as pd
import math


class Evolve:
    battle_time = 0
    reproduction_time = 0

    population = []
    fitness_dict = {}
    starting_elo = 1000

    output = None

    @staticmethod
    def evolve():
        tick = time.clock()
        print("GENERATING INITIAL TEAMS!")
        Evolve.population = [Metagame.generate_team(Model.core) for _ in range(0, Model.population_size)]
        print("EVOLVING!")
        for generation in range(0, Model.num_generations):
            tick = time.clock()
            Model.mutation_prob = max(0, Model.starting_mutation_rate + generation * Model.mutation_delta)
            Evolve.next_generation()
            print("GENERATION", generation, "took", time.clock() - tick)
        print("ELITES!")
        Evolve.final_evaluation()
        print("TOTAL TIME IN EVOLUTION:", time.clock() - tick)
        print("BATTLE TIME:", Evolve.battle_time)
        print("REPRODUCTION TIME:", Evolve.reproduction_time)

    @staticmethod
    def next_generation():

        tack = time.clock()
        # grab |matches| sample of norms
        norm_choices = [key for key in Model.elo_dict]
        norms = np.random.choice(norm_choices, Model.matches)

        # battles all norms against team, returns elo
        def fitness(team):
            elo = Evolve.starting_elo
            for norm in norms:
                winner = Damage.battle(team, norm)
                norm_elo = Model.elo_dict[norm]
                elo = Elo.update_elo(elo, norm_elo, winner)
            return Elo.win_prob(elo)

        Evolve.fitness_dict = {team: fitness(team) for team in Evolve.population}
        tick = time.clock()
        print(Model.matches * Model.population_size, "battles took", tick - tack)
        Evolve.battle_time += tick - tack

        choices = [key for key in Evolve.fitness_dict]
        weights = [Evolve.fitness_dict[key] for key in Evolve.fitness_dict]
        total_weight = sum(weights)
        weights = [weight / total_weight for weight in weights]

        def get_newborn():
            parents = np.random.choice(choices, 2, p=weights)
            return Team.reproduce(parents[0], parents[1])

        elites = Evolve.get_elites()
        mutants = [get_newborn() for _ in range(0, Model.population_size - len(elites))]
        Evolve.population = elites + mutants
        tock = time.clock()
        Evolve.reproduction_time += tock - tick

    @staticmethod
    def get_elites():
        elites = sorted(Evolve.fitness_dict,
                        key=Evolve.fitness_dict.get,
                        reverse=True)[:math.floor(Model.population_size / 10)]
        return [team.get_elite() for team in elites]

    @staticmethod
    def final_evaluation():
        # grab |matches| sample of norms
        norm_choices = [key for key in Model.elo_dict]

        # battles all norms against team, returns elo
        def precise_fitness(team, num_norms=len(norm_choices)):
            norms = np.random.choice(norm_choices, num_norms)
            elo = Evolve.starting_elo
            for norm in norms:
                winner = Damage.battle(team, norm)
                norm_elo = Model.elo_dict[norm]
                elo = Elo.update_elo(elo, norm_elo, winner)
            return elo

        Evolve.fitness_dict = {team: precise_fitness(team, 50) for team in Evolve.population}
        Evolve.output = sorted(Evolve.fitness_dict, key=Evolve.fitness_dict.get, reverse=True)[:10]
        for team in Evolve.output:
            Evolve.fitness_dict[team] = precise_fitness(team, 200)

    @staticmethod
    def get_best():
        maximum = max(Evolve.fitness_dict, key=Evolve.fitness_dict.get)
        print("EVOLUTION OUTPUT:")
        print(maximum, Evolve.fitness_dict[maximum])
        return Evolve.fitness_dict[maximum]

    @staticmethod
    def write_to_file():
        output_df = pd.DataFrame(list(Evolve.fitness_dict.items()), columns=["Team", "Elo"])
        Writer.save_csv_object(output_df, "result.csv")
