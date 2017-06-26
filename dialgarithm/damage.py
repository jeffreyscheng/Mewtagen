from Writer import *
import math
import numpy as np


class Damage:
    @staticmethod
    def start():
        Damage.read_damage_cache()
        Damage.get_all_counters()
        Damage.get_switches()
        Damage.get_attack()

    @staticmethod
    def end():
        Writer.save_pickled_object(Dialgarithm.attack_cache, 'attack.txt')
        # Writer.save_pickled_object(Dialgarithm.time_list, 'time_list.txt')
        Writer.save_csv_object(Dialgarithm.damage_cache, 'damage.csv')
        Writer.save_csv_object(Dialgarithm.switch_cache, 'switch.csv')

    @staticmethod
    def get_all_counters():
        tentative_counters = Writer.load_pickled_object('counters.txt')
        if tentative_counters is None:
            Dialgarithm.counters_dict =\
                {moveset: Damage.get_counters_of_moveset(moveset)
                 for moveset in Dialgarithm.moveset_list}
            Writer.save_pickled_object(Dialgarithm.counters_dict,
                                       'counters.txt')
        else:
            Dialgarithm.counters_dict = tentative_counters

    @staticmethod
    def get_switches():
        tentative_switches = Writer.load_csv_object('switch.csv')
        if tentative_switches is None:
            n = len(Dialgarithm.moveset_list)
            arr = np.zeros((n, n))
            arr[:] = np.nan
            Dialgarithm.switch_cache =\
                pd.DataFrame(data=arr, index=Dialgarithm.moveset_dict.keys(),
                             columns=Dialgarithm.moveset_dict.keys())
        else:
            Dialgarithm.switch_cache = tentative_switches

    @staticmethod
    def get_attack():
        tentative_attack = Writer.load_pickled_object('attack.txt')
        if tentative_attack is None:
            Dialgarithm.attack_cache = {}
        else:
            Dialgarithm.attack_cache = tentative_attack

    @staticmethod
    def read_damage_cache():
        tentative_cache = Writer.load_csv_object('damage.csv')
        if tentative_cache is None:
            n = len(Dialgarithm.moveset_list)
            arr = np.zeros((n, n))
            arr[:] = np.nan
            Dialgarithm.damage_cache =\
                pd.DataFrame(data=arr, index=Dialgarithm.moveset_dict.keys(),
                             columns=Dialgarithm.moveset_dict.keys())
        else:
            Dialgarithm.damage_cache = tentative_cache

    @staticmethod
    def deal_damage(attacker, defender):
        if not np.isnan(Dialgarithm.damage_cache.loc[attacker.name,
                                                     defender.name]):
            return Dialgarithm.damage_cache.loc[attacker.name, defender.name]
        else:
            damage_list = [Damage.move_damage(attacker,
                                              defender,
                                              Dialgarithm.dex.move_dict[move])
                           for move in attacker.moves]
            damage = max(damage_list)
            Dialgarithm.damage_cache.loc[attacker.name, defender.name] = damage
            return damage

    @staticmethod
    def get_damage_switch(attacker, switcher, defender):
        m_dict = Dialgarithm.dex.move_dict
        damage_dict = {m_dict[move]: Damage.move_damage(attacker,
                                                        switcher,
                                                        m_dict[move])
                       for move in attacker.moves}
        best_move = max(damage_dict, key=damage_dict.get)
        damage = Damage.move_damage(attacker, defender, best_move)
        return damage

    @staticmethod
    def get_weighted_switch_damage(outgoing, victim):
        if not np.isnan(Dialgarithm.switch_cache.loc[outgoing.name,
                                                     victim.name]):
            return Dialgarithm.switch_cache.loc[outgoing.name, victim.name]
        else:
            u = Dialgarithm.usage_dict
            c = Dialgarithm.counters_dict
            if outgoing == victim:
                # outgoing_set = Dialgarithm.moveset_dict[outgoing]
                contributions = [
                    (u[mon.pokemon.unique_name],
                     Damage.get_damage_switch(mon, outgoing, victim))
                    for mon in Dialgarithm.moveset_list
                    if mon not in Dialgarithm.counters_dict[outgoing]]
            else:
                contributions = [(u[mon.pokemon.unique_name],
                                  Damage.get_damage_switch(mon,
                                                           outgoing,
                                                           victim))
                                 for mon in c[outgoing] if
                                 mon not in c[victim]]
                if sum([a for a, b in contributions]) == 0:
                    contributions = [
                        (Dialgarithm.usage_dict[mon.pokemon.unique_name],
                         Damage.get_damage_switch(mon, outgoing, victim))
                        for mon in Dialgarithm.moveset_list]
            numerator = sum([a * b for a, b in contributions])
            denominator = sum([a for a, b in contributions])
            weighted_damage = numerator / denominator
            s = Dialgarithm.switch_cache
            s.loc[outgoing.name, victim.name] = weighted_damage
            return weighted_damage

    @staticmethod
    def get_weighted_attack_damage(attacker_name):
        attacker_set = Dialgarithm.moveset_dict[attacker_name]
        if attacker_name in Dialgarithm.attack_cache:
            return Dialgarithm.attack_cache[attacker_name]
        else:
            u = Dialgarithm.usage_dict
            contributions = [(u[mon.pokemon.unique_name],
                              Damage.deal_damage(attacker_set, mon))
                             for mon in Dialgarithm.moveset_list]
            weighted_attack = sum([a * b for a, b in contributions])
            Dialgarithm.attack_cache[attacker_name] = weighted_attack
            return weighted_attack

    @staticmethod
    def move_damage(attacker, defender, move):
        if move.name == 'Seismic Toss':
            return 100 / defender.hp_stat
        move_type = Dialgarithm.dex.type_dict[move.type]
        type_coefficients = [move_type.effects[def_type]
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
        special_factors = coefficient * move.accuracy / 100.0 * 0.925
        power_factors = attacker_atk / defender_def * move.base_power
        damage = (210 / 250 * power_factors + 2) * special_factors
        return damage / defender.hp_stat

    @staticmethod
    def check_counter(yours, theirs):
        damage_to_yours = Damage.deal_damage(theirs, yours)
        damage_to_theirs = Damage.deal_damage(yours, theirs)
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
            return turns_to_kill_theirs > turns_to_kill_yours + 1

    @staticmethod
    def get_counters_of_moveset(moveset):
        print(moveset.name)
        counters = [m_set for m_set in Dialgarithm.moveset_list
                    if Damage.check_counter(moveset, m_set)]
        return counters

    @staticmethod
    def battle(team1, team2):
        tick = time.clock()
        team1.heal()
        team2.heal()
        team1.current = random.choice(list(team1.party.keys()))
        team2.current = random.choice(list(team2.party.keys()))

        while team1.still_playing() and team2.still_playing():
            if team1.is_fainted() or team1.current is None:
                team1.switch()
            if team2.is_fainted() or team2.current is None:
                team2.switch()
            d = Dialgarithm.counters_dict
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
                    team2.damage_current(Damage.deal_damage(team1.current,
                                                            team2.current))
                    if not team2.is_fainted():
                        team1.damage_current(Damage.deal_damage(team2.current,
                                                                team1.current))
                else:
                    team1.damage_current(Damage.deal_damage(team2.current,
                                                            team1.current))
                    if not team1.is_fainted():
                        team2.damage_current(Damage.deal_damage(team1.current,
                                                                team2.current))

            # Case 1: both stay
            if (not bool_1_counters_2) and (not bool_2_counters_1):
                normal_damage()

            # Case 2: 1 stays, 2 switches
            elif bool_1_counters_2:
                if team2.has_living_counter(team1.current):
                    team2.switch(team1.current)
                    team2.damage_current(Damage.deal_damage(team1.current,
                                                            team2.current))
                else:
                    normal_damage()

            # Case 3: 2 stays, 1 leaves
            elif bool_2_counters_1:
                if team1.has_living_counter(team2.current):
                    team1.switch(team2.current)
                    team1.damage_current(Damage.deal_damage(team2.current,
                                                            team1.current))
                else:
                    normal_damage()

            # Case 4: both switch
            # I don't think this should ever happen?
            else:
                print('These two Pokemon counter each other somehow')
                print(team1.current.name)
                print(team2.current.name)
                raise RuntimeError("two mons counter each other, both switch?")
        tock = time.clock()
        print('BATTLE FINISHED IN: ' + str(tock - tick) + ' seconds.')
        if team1.still_playing():
            return team1
        else:
            return team2
