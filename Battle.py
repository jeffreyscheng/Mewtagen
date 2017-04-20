from Writer import *
from Team import *
import random
import math
import numpy as np
import time


class Battle:
    def __init__(self):
        tentative_cache = Writer.load_object('damage.txt')
        if tentative_cache is None:
            Dialgarithm.damage_cache = {}
        else:
            Dialgarithm.damage_cache = tentative_cache
        self.moveset_list = [mon for name, mon in Dialgarithm.moveset_dict.items()]

    def battle(self, team1, team2):
        tick = time.clock();
        team1.heal()
        team2.heal()
        team1.current = random.choice(list(team1.party.keys()))
        team2.current = random.choice(list(team2.party.keys()))

        while team1.still_playing() and team2.still_playing():
            if team1.is_fainted() or team1.current is None:
                team1.switch()
            if team2.is_fainted() or team2.current is None:
                team2.switch()
            bool_1_counters_2 = team1.current in Dialgarithm.counters_dict[team2.current]
            bool_2_counters_1 = team2.current in Dialgarithm.counters_dict[team1.current]

            def normal_damage():
                if team1.current.spe_stat > team2.current.spe_stat:
                    team1_moves_first = True
                elif team1.current.spe_stat < team2.current.spe_stat:
                    team1_moves_first = False
                else:
                    team1_moves_first = random.choice([0, 1])
                if team1_moves_first:
                    team2.damage_current(self.deal_damage(team1.current, team2.current))
                    if not team2.is_fainted():
                        team1.damage_current(self.deal_damage(team2.current, team1.current))
                else:
                    team1.damage_current(self.deal_damage(team2.current, team1.current))
                    if not team1.is_fainted():
                        team2.damage_current(self.deal_damage(team1.current, team2.current))


            # Case 1: both stay
            if (not bool_1_counters_2) and (not bool_2_counters_1):
                normal_damage()

            # Case 2: 1 stays, 2 switches
            elif bool_1_counters_2:
                if team2.has_living_counter(team1.current):
                    team2.switch(team1.current)
                    team2.damage_current(self.deal_damage(team1.current, team2.current))
                else:
                    normal_damage()

            # Case 3: 2 stays, 1 leaves
            elif bool_2_counters_1:
                if team1.has_living_counter(team2.current):
                    team1.switch(team2.current)
                    team1.damage_current(self.deal_damage(team2.current, team1.current))
                else:
                    normal_damage()

            # Case 4: both switch
            # I don't think this should ever happen?
            else:
                print('These two Pokemon counter each other somehow')
                print(team1.current.name)
                print(team2.current.name)
                raise RuntimeError("two mons counter each other, both switch?")
        tock = time.clock();
        print('BATTLE FINISHED IN: ' + str(tock - tick) + ' seconds.')
        if team1.still_playing():
            return team1
        else:
            return team2

    def deal_damage(self, attacker, defender):
        pair = attacker, defender
        if pair in Dialgarithm.damage_cache:
            return Dialgarithm.damage_cache[pair]
        else:
            damage_list = [Battle.move_damage(attacker, defender, Dialgarithm.dex.move_dict[move])
                           for move in attacker.moves]
            damage = max(damage_list)
            tup = attacker, defender
            Dialgarithm.damage_cache[tup] = damage
            return damage

    @staticmethod
    def move_damage(attacker, defender, move):
        move_type = Dialgarithm.dex.type_dict[move.type]
        type_coefficients = [move_type.effects[def_type] for def_type in defender.pokemon.types]
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
        damage = (210 / 250 * attacker_atk / defender_def * move.base_power + 2) * coefficient * move.accuracy / 100.0 * 0.925
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
        if turns_to_kill_yours == turns_to_kill_theirs - 1:
            your_speed = yours.spe_stat
            their_speed = theirs.spe_stat
            return their_speed > your_speed
        else:
            return turns_to_kill_yours < turns_to_kill_theirs - 1

    def get_counters_of_moveset(self, moveset):
        print(moveset.name)
        return [m_set for m_set in self.moveset_list if self.check_counter(moveset, m_set)]

    def get_all_counters(self):
        tentative_counters = Writer.load_object('counters.txt')
        if tentative_counters is None:
            Dialgarithm.counters_dict = {moveset: self.get_counters_of_moveset(moveset) for moveset in
                                         self.moveset_list}
            Writer.save_object(Dialgarithm.counters_dict, 'counters.txt')
        else:
            Dialgarithm.counters_dict = tentative_counters
