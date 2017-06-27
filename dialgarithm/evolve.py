from .metagame import *

class Evolve:
    population_size = 500
    generations = 100
    population = {}

    def evolve(self):
        print("GENERATING TEAMS!")
        number_of_teams = 500
        starting_elo = 1000
        population = {Metagame.generate_team(Model.core): starting_elo for _ in range(0, number_of_teams)}
        seconds_spent = Model.time
        counter = 0

        # damage - 1800, switch - 1000

        def sample_by_elo(elo_distribution):
            r = random.uniform(0, 1000 * number_of_teams)
            runner = 0
            for key, value in elo_distribution.items():
                if runner + value >= r:
                    return key
                runner += value
            assert False, "Shouldn't get here"

        # each cycle takes roughly 15 seconds
        print("BEGINNING CYCLES")
        while time.clock() - tick < seconds_spent:
            for i in range(0, 30):
                counter += 1
                # sort by elo
                bracket = sorted(population,
                                 key=population.get)
                # pair off and battle down the line
                for i in range(0, number_of_teams // 2):
                    team1 = bracket[2 * i]
                    team2 = bracket[2 * i + 1]
                    self.run_battle(team1, team2)
            print("NEW POPULATION")
            winners = [sample_by_elo(population) for i
                       in range(0, number_of_teams)]
            population = \
                {team.reproduce(): population[team]
                 for team in winners}

        print("DONE BATTLING, ANALYZING")
        [t.analyze() for t in population.keys()]
        suggestions = sorted(population,
                             key=population.get)[0:3]
        print("SUGGESTIONS:")
        for suggestion in suggestions:
            suggestion.display()
