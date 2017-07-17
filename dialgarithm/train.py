from .evolve import *
import math


class Train:
    time_per_battle = 20 / 1000  # from EC2 instance and personal laptop
    target_time = 5 * 60

    @staticmethod
    def run_parameter_set(population_size, matches, starting_mutation_rate, mutation_delta):
        population_size = math.floor(population_size)
        matches = math.floor(matches)
        time_for_final_evaluation = Train.time_per_battle * population_size * 25
        time_for_evolution = Train.target_time - time_for_final_evaluation
        if time_for_evolution <= 0 or population_size <= 0 or matches <= 0 or starting_mutation_rate <= 0:
            print("not enough time!")
            print(time_for_final_evaluation)
            return 0
        else:
            time_per_generation = population_size * matches * Train.time_per_battle
            num_generations = math.floor(time_for_evolution / time_per_generation)
            print(num_generations)

            # TODO: DO THING SOMETHING FUNCTION
            def something(a, b, c, d, e):
                pass

            return something(population_size, matches, num_generations, starting_mutation_rate, mutation_delta)

    # TODO: THIS
    @staticmethod
    def optimize_parameters():
        pass