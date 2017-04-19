from Writer import *
import random
import math
import numpy as np
import time


class Battle:
    def __init__(self):
        tentative_cache = Writer.load_object('damage_cache.txt')
        if tentative_cache is None:
            self.damage_cache = {}
        else:
            self.damage_cache = tentative_cache

    def battle(self, team1, team2):
        tick = time.clock()
        team1.heal()
        team2.heal()
        team1.current = random.choice(team1.party.keys())
        team2.current = random.choice(team2.party.keys())
        counters_to_team1 = {moveset1: [moveset2 for moveset2 in team2.party.keys() if moveset2
                                        in Dialgarithm.counters_dict[moveset1]] for moveset1 in team1.party.keys()}
        counters_to_team2 = {moveset1: [moveset2 for moveset2 in team1.party.keys() if moveset2
                                        in Dialgarithm.counters_dict[moveset1]] for moveset1 in team2.party.keys()}

        # def helper(curr1, curr2):
        #     tock = time.clock()
        #     if tock - tick > 30:
        #         print(team1)
        #         print(team2)
        #         print(team1_health)
        #         print(team2_health)
        #         print(current1)
        #         print(current2)
        #     bool_1_counters_2 = team1[curr1] in self.counters[team2[curr2]]
        #     # this line literally takes the majority of the time -- optimize, dummy
        #     # bool_1_counters_2 = self.check_counter(team1[curr1], team2[curr2], team1_health[curr1], team2_health[curr2])
        #     turn_team1_used = False
        #     turn_team2_used = False
        #
        #     if bool_1_counters_2:
        #         # curr1 stays in for sure, curr2 may switch out
        #         if len(counters_to_team1[curr1]) > 0:
        #             check = random.randint(1, 10)
        #             if check < 10:
        #                 curr2 = random.choice(counters_to_team1[curr1])
        #                 turn_team2_used = True
        #     else:
        #         if len(counters_to_team2[curr2]) > 0:
        #             check = random.randint(1, 10)
        #             if check < 10:
        #                 curr1 = random.choice(counters_to_team2[curr2])
        #                 turn_team1_used = True
        #
        #     def team_1_attacks(c1, c2):
        #         team2_health[c2] -= self.deal_damage(team1[c1], team2[c2]) / self.get_stat(team2[c2], 'hp')
        #         if team2_health[c2] <= 0:
        #             team2_health[c2] = 0
        #             try:
        #                 counters_to_team1[curr1].remove(c2)
        #             except ValueError:
        #                 pass
        #             if sum(team2_health) > 0:
        #                 if len(counters_to_team1[curr1]) > 0:
        #                     c2 = random.choice(counters_to_team1[curr1])
        #                 else:
        #                     c2 = next(x[0] for x in enumerate(team2_health) if x[1] > 0)
        #         return c1, c2
        #
        #     def team_2_attacks(c1, c2):
        #         team1_health[c1] -= self.deal_damage(team2[c2], team1[c1]) / self.get_stat(team1[c1], 'hp')
        #         if team1_health[c1] <= 0:
        #             team1_health[c1] = 0
        #             try:
        #                 counters_to_team2[curr2].remove(c1)
        #             except ValueError:
        #                 pass
        #             if sum(team1_health) > 0:
        #                 if len(counters_to_team2[curr2]) > 0:
        #                     c1 = random.choice(counters_to_team2[curr2])
        #                 else:
        #                     c1 = next(x[0] for x in enumerate(team1_health) if x[1] > 0)
        #         return c1, c2
        #
        #     old_c1 = curr1
        #     old_c2 = curr2
        #
        #     if self.get_stat(team1[curr1], 'spd') > self.get_stat(team2[curr2], 'spd'):
        #         if not turn_team1_used:
        #             curr1, curr2 = team_1_attacks(curr1, curr2)
        #         if old_c2 == curr2 and not turn_team2_used:
        #             curr1, curr2 = team_2_attacks(curr1, curr2)
        #     else:
        #         if not turn_team2_used:
        #             curr1, curr2 = team_2_attacks(curr1, curr2)
        #         if old_c1 == curr1 and not turn_team1_used:
        #             curr1, curr2 = team_1_attacks(curr1, curr2)
        #     return curr1, curr2
        #
        # while sum(team1_health) > 0 and sum(team2_health) > 0:
        #     current1, current2 = helper(current1, current2)
        # return sum(team1_health) > 0

    def deal_damage(self, attacker, defender):
        pair = attacker, defender
        if pair in self.damage_cache:
            return self.damage_cache[pair]
        else:
            damage_list = [Battle.move_damage(attacker, defender, Move(move)) for move in attacker.moves]
            return max(damage_list)

    @staticmethod
    def move_damage(attacker, defender, move):
        move_type = Dialgarithm.dex.move_dict[move.type]
        type_coefficients = [move_type.type_coefficient[Dialgarithm.dex.move_dict[def_type]]
                             for def_type in defender.pokemon.types]
        coefficient = np.product(type_coefficients)

        # record abilities and items, you dummy

        if move.category == 'Physical':
            if move.name == 'Foul Play':
                attacker_atk = defender.atk_stat
                defender_def = defender.def_stat
            elif move.name == 'Knock Off':
                attacker_atk = 1.5 * attacker.atk_stat
                defender_def = defender.def_stat
            else:
                attacker_atk = attacker.atk_stat
                defender_def = defender.def_stat
        else:
            if move.name == 'Psyshock':
                attacker_atk = attacker.spa_stat
                defender_def = defender.def_stat
            else:
                attacker_atk = attacker.spa_stat
                defender_def = defender.spd_stat
        damage = (
                     210 / 250 * attacker_atk / defender_def * move.base_power + 2) * coefficient * move.accuracy / 100.0 * 0.925
        if damage >= defender.hp_stat:
            return 1
        else:
            return damage / defender.hp_stat

    def check_counter(self, yours, theirs):
        damage_to_yours = self.deal_damage(theirs, yours)
        damage_to_theirs = self.deal_damage(yours, theirs)
        if damage_to_theirs == 0:
            return True
        elif damage_to_yours == 0:
            return False
        turns_to_kill_yours = math.ceil(yours.hp_stat / damage_to_yours)
        turns_to_kill_theirs = math.ceil(theirs.hp_stat / damage_to_theirs)
        if turns_to_kill_yours == turns_to_kill_theirs + 1:
            your_speed = self.get_stat(yours, 'spe')
            their_speed = self.get_stat(theirs, 'spe')
            return their_speed > your_speed
        else:
            return turns_to_kill_yours > turns_to_kill_theirs + 1

    def get_counters_of_moveset(self, moveset):
        return [m_set for m_set in Dialgarithm.moveset_list if self.check_counter(moveset, m_set)]

    def get_all_counters(self):
        tentative_counters = Writer.load_object('counters.txt')
        if tentative_counters is None:
            Dialgarithm.counters_dict = {moveset: self.get_counters_of_moveset(moveset) for moveset in
                                         Dialgarithm.moveset_list}
            Writer.save_object(Dialgarithm.counters_dict, 'counters.txt')
        else:
            Dialgarithm.counters_dict = tentative_counters
