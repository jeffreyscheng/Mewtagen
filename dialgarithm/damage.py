from .Writer import *
import math
import numpy as np
import time
import random


class Damage:
    @staticmethod
    def start():
        # Damage.read_damage_cache()
        Damage.get_all_counters()
        Damage.get_mutations()
        # Damage.read_switch_cache()
        # Damage.get_switches()
        # Damage.get_attack()
        # @staticmethod
        # def end():
        #     # Writer.save_pickled_object(Model.attack_cache, 'attack.txt')
        #     # Writer.save_pickled_object(Model.damage_cache, 'damage.txt')
        #     # Writer.save_pickled_object(Model.mutation_dict, 'mutation.txt')
        #     # Writer.save_csv_object(Model.switch_cache, 'switch.csv')
        #     pass

    @staticmethod
    def get_all_counters():
        tentative_counters = Writer.load_pickled_object('counters.txt')
        if tentative_counters is None:
            Model.counters_dict = \
                {moveset: Damage.get_counters_of_moveset(moveset)
                 for moveset in Model.moveset_list}
            Writer.save_pickled_object(Model.counters_dict,
                                       'counters.txt')
        else:
            Model.counters_dict = tentative_counters

    @staticmethod
    def read_damage_cache():
        tentative_cache = Writer.load_pickled_object('damage.txt')
        if tentative_cache is None:
            tick = time.clock()
            print("Caching damage...")
            tentative_cache = {}
            for mon in Model.moveset_list:
                for mon2 in Model.moveset_list:
                    key = mon.name, mon2.name
                    value = Damage.deal_damage(mon, mon2)
                    tentative_cache[key] = value
            print("Damage took", time.clock() - tick)
        Model.damage_cache = tentative_cache

    @staticmethod
    def read_move_cache():
        tentative_cache = Writer.load_pickled_object('move_cache.txt')
        if tentative_cache is None:
            tentative_cache = {}
            tick = time.clock()
            print("Caching moves...")

            def get_best_move(attack_mon, switch_mon):
                m_dict = Model.dex.move_dict
                damage_dict = {m_dict[move]: Damage.move_damage(attack_mon,
                                                                switch_mon,
                                                                m_dict[move])
                               for move in attack_mon.movess}
                return max(damage_dict, key=damage_dict.get)

            for attacker in Model.moveset_list:
                tick = time.clock()
                print(attacker.name)
                switchers = [mon for mon in Model.moveset_list if attacker in Model.counters_dict[mon]]
                for switcher in switchers:
                    key = attacker.name, switcher.name
                    tentative_cache[key] = get_best_move(attacker, switcher)
                print(time.clock() - tick)
            print("Moves took", time.clock() - tick)
            Writer.save_pickled_object(tentative_cache, 'move_cache.txt')
        Model.move_cache = tentative_cache

    @staticmethod
    def read_switch_cache():
        tentative_cache = Writer.load_pickled_object('switch_cache.txt')
        if tentative_cache is None:
            tentative_cache = {}
            tick = time.clock()
            print("Caching switch...")
            for attacker in Model.moveset_list:
                tick = time.clock()
                print(attacker.name)
                defenders = [mon for mon in Model.moveset_list if attacker not in Model.counters_dict[mon]]
                for move in attacker.moves:
                    for defender in defenders:
                        key = attacker.name, move, defender.name
                        tentative_cache[key] = Damage.move_damage(attacker, defender, move)
                print(time.clock() - tick)
                print(len(defenders), 'defenders')
            print("Switches took", time.clock() - tick)
            Writer.save_pickled_object(tentative_cache, 'switch_cache.txt')
        Model.switch_cache = tentative_cache

    @staticmethod
    def deal_damage(attacker, defender):
        # tuple_key = attacker.name, defender.name
        # if tuple_key in Model.damage_cache:
        #     return Model.damage_cache[tuple_key]
        # else:
        damage_list = [Damage.move_damage(attacker,
                                          defender,
                                          Model.dex.move_dict[move])
                       for move in attacker.moves]
        damage = max(damage_list)
        return damage

    @staticmethod
    def get_damage_switch(attacker, switcher, defender):
        # move = Model.move_cache[attacker.name, switcher.name]
        # return Model.switch_cache[attacker.name, move, defender.name]
        m_dict = Model.dex.move_dict
        damage_dict = {m_dict[move]: Damage.move_damage(attack_mon,
                                                        switch_mon,
                                                        m_dict[move])
                       for move in attacker.movess}
        best = max(damage_dict, key=damage_dict.get)
        return Damage.move_damage(attacker, defender, best)

    @staticmethod
    def move_damage(attacker, defender, move):
        if move.name == 'Seismic Toss':
            return 100 / defender.hp_stat
        move_type = Model.dex.type_dict[move.type]
        type_coefficients = [move_type.effects[def_type]
                             for def_type in defender.pokemon.types]
        coefficient = np.product(type_coefficients)
        if move_type.name in attacker.pokemon.types:
            stab = 1.5
        else:
            stab = 1

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
        special_factors = coefficient * move.accuracy / 100.0 * stab
        power_factors = attacker_atk / defender_def * move.base_power
        damage = (42 * power_factors / 50 + 2) * special_factors * 0.925  # .925 = avg rand
        return damage / defender.hp_stat

    @staticmethod
    def check_counter(yours, theirs):
        damage_to_yours = Damage.deal_damage(theirs, yours)
        damage_to_theirs = Damage.deal_damage(yours, theirs)
        if damage_to_theirs == 0:
            return True
        elif damage_to_yours == 0:
            return False
        turns_to_kill_yours = math.ceil(1 / damage_to_yours)
        turns_to_kill_theirs = math.ceil(1 / damage_to_theirs)
        if turns_to_kill_yours == turns_to_kill_theirs - 1:
            your_speed = yours.spe_stat
            their_speed = theirs.spe_stat
            return their_speed > your_speed
        else:
            return turns_to_kill_theirs > turns_to_kill_yours + 1

    @staticmethod
    def get_counters_of_moveset(moveset):
        print(moveset.name)
        counters = [m_set for m_set in Model.moveset_list
                    if Damage.check_counter(moveset, m_set)]
        return counters

    @staticmethod
    def battle(team1, team2, log=False):
        team1.heal()
        team2.heal()
        team1.switch()
        team2.switch()
        # Writer.log("Team 1 started with", team1.current.name)
        # Writer.log("Team 2 started with", team2.current.name)

        while team1.still_playing() and team2.still_playing():
            if team1.is_fainted() or team1.current is None:
                team1.switch()
                # Writer.log("Team 1 switched to", team1.current.name)
            if team2.is_fainted() or team2.current is None:
                team2.switch()
                # Writer.log("Team 2 switched to", team2.current.name)
            d = Model.counters_dict
            bool_1_counters_2 = team1.current in d[team2.current]
            bool_2_counters_1 = team2.current in d[team1.current]

            def normal_damage():
                if team1.current.spe_stat > team2.current.spe_stat:
                    team1_moves_first = True
                elif team1.current.spe_stat < team2.current.spe_stat:
                    team1_moves_first = False
                else:
                    team1_moves_first = random.choice([0, 1])
                if team1_moves_first:
                    team2.damage_current(Damage.deal_damage(team1.current, team2.current))
                    # Writer.log("Team 1's", team1.current.name, "attacks", team2.current.name, "first for",
                    #            str(Damage.deal_damage(team1.current, team2.current)), "damage.")
                    if not team2.is_fainted():
                        team1.damage_current(Damage.deal_damage(team2.current,
                                                                team1.current))
                        # Writer.log("Team 2's", team2.current.name, "survives and attacks", team1.current.name,
                        #            "second for", str(Damage.deal_damage(team2.current, team1.current)), "damage.")
                        # else:
                        # Writer.log("Team 2's", team2.current.name, "fainted.")
                else:
                    # Writer.log("Team 2's", team2.current.name, "attacks", team1.current.name, "first for",
                    #            str(Damage.deal_damage(team2.current, team1.current)), "damage.")
                    team1.damage_current(Damage.deal_damage(team2.current,
                                                            team1.current))
                    if not team1.is_fainted():
                        # Writer.log("Team 1's", team1.current.name, "survives and attacks", team2.current.name,
                        #            "second for", str(Damage.deal_damage(team1.current, team2.current)), "damage.")
                        team2.damage_current(Damage.deal_damage(team1.current,
                                                                team2.current))
                        # else:
                        # Writer.log("Team 1's", team1.current.name, "fainted.")

            # Case 1: both stay
            if (not bool_1_counters_2) and (not bool_2_counters_1):
                # Writer.log("Normal damage:")
                normal_damage()

            # Case 2: 1 stays, 2 switches
            elif bool_1_counters_2:
                # Writer.log("Team 1 stays, Team 2 switches")
                if team2.has_living_counter(team1.current):
                    team2.switch(team1.current)
                    # Writer.log("Team 2 switches to", team2.current.name)
                    team2.damage_current(Damage.deal_damage(team1.current, team2.current))
                    # Writer.log("Team 1's", team1.current.name, "deals",
                    #            str(Damage.deal_damage(team1.current, team2.current)), "to", team2.current.name)
                else:
                    normal_damage()

            # Case 3: 2 stays, 1 leaves
            elif bool_2_counters_1:
                # Writer.log("Team 1 switches, Team 2 stays")
                if team1.has_living_counter(team2.current):
                    # Writer.log("Team 1 switches to", team1.current.name)
                    team1.switch(team2.current)
                    team1.damage_current(Damage.deal_damage(team2.current,
                                                            team1.current))
                    # Writer.log("Team 2's", team2.current.name, "deals",
                    #            str(Damage.deal_damage(team2.current, team1.current)), "to", team1.current.name)
                else:
                    normal_damage()

            # Case 4: both switch
            # I don't think this should ever happen?
            else:
                print('These two Pokemon counter each other somehow')
                print(team1.current.name)
                print(team2.current.name)
                raise RuntimeError("two mons counter each other, both switch?")
        if team1.still_playing():
            # Writer.log("Team 1 won!")
            return True
        else:
            # Writer.log("Team 2 won!")
            return False

    @staticmethod
    def rand_bat(team1, team2):
        return random.random() > 0.5

    @staticmethod
    def get_mutations():
        tentative_mutations = Writer.load_pickled_object('mutation.txt')
        if tentative_mutations is None:
            print("Getting mutations...")
            tick = time.clock()
            Model.mutation_dict = {moveset: moveset.compute_mutation() for moveset in Model.moveset_list}
            print("Mutations took", time.clock() - tick)
        else:
            Model.mutation_dict = tentative_mutations
