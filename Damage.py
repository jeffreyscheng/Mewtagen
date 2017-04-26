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
        Writer.save_pickled_object(Dialgarithm.time_list, 'time_list.txt')
        Writer.save_csv_object(Dialgarithm.damage_cache, 'damage.csv')
        Writer.save_csv_object(Dialgarithm.switch_cache, 'switch.csv')

    @staticmethod
    def get_all_counters():
        tentative_counters = Writer.load_pickled_object('counters.txt')
        if tentative_counters is None:
            Dialgarithm.counters_dict = {moveset: Damage.get_counters_of_moveset(moveset) for moveset in
                                         Dialgarithm.moveset_list}
            Writer.save_pickled_object(Dialgarithm.counters_dict, 'counters.txt')
        else:
            Dialgarithm.counters_dict = tentative_counters

    @staticmethod
    def get_switches():
        tentative_switches = Writer.load_csv_object('switch.csv')
        if tentative_switches is None:
            n = len(Dialgarithm.moveset_list)
            arr = np.zeros((n, n))
            arr[:] = np.nan
            Dialgarithm.switch_cache = pd.DataFrame(data=arr, index=Dialgarithm.moveset_dict.keys(),
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
            Dialgarithm.damage_cache = pd.DataFrame(data=arr, index=Dialgarithm.moveset_dict.keys(),
                                                    columns=Dialgarithm.moveset_dict.keys())
        else:
            Dialgarithm.damage_cache = tentative_cache

    @staticmethod
    def deal_damage(attacker, defender):
        if not np.isnan(Dialgarithm.damage_cache.loc[attacker.name, defender.name]):
            return Dialgarithm.damage_cache.loc[attacker.name, defender.name]
        else:
            damage_list = [Damage.move_damage(attacker, defender, Dialgarithm.dex.move_dict[move])
                           for move in attacker.moves]
            damage = max(damage_list)
            Dialgarithm.damage_cache.loc[attacker.name, defender.name] = damage
            return damage

    @staticmethod
    def get_damage_switch(attacker, switcher, defender):
        m_dict = Dialgarithm.dex.move_dict
        damage_dict = {m_dict[move]: Damage.move_damage(attacker, switcher, m_dict[move])
                       for move in attacker.moves}
        best_move = max(damage_dict, key=damage_dict.get)
        damage = Damage.move_damage(attacker, defender, best_move)
        return damage

    @staticmethod
    def get_weighted_switch_damage(outgoing, victim):
        if not np.isnan(Dialgarithm.switch_cache.loc[outgoing.name, victim.name]):
            return Dialgarithm.switch_cache.loc[outgoing.name, victim.name]
        else:
            if outgoing == victim:
                # outgoing_set = Dialgarithm.moveset_dict[outgoing]
                contributions = [
                    (Dialgarithm.usage_dict[mon.pokemon.unique_name], Damage.get_damage_switch(mon, outgoing, victim))
                    for mon in Dialgarithm.moveset_list if mon not in Dialgarithm.counters_dict[outgoing]]
            else:
                contributions = [(Dialgarithm.usage_dict[mon.pokemon.unique_name],
                                  Damage.get_damage_switch(mon, outgoing, victim))
                                 for mon in Dialgarithm.counters_dict[outgoing] if
                                 mon not in Dialgarithm.counters_dict[victim]]
                if sum([a for a, b in contributions]) == 0:
                    # just to make sure stuff doesn't break if one counter set is a superset of another
                    contributions = [
                        (Dialgarithm.usage_dict[mon.pokemon.unique_name],
                         Damage.get_damage_switch(mon, outgoing, victim))
                        for mon in Dialgarithm.moveset_list]
            weighted_damage = sum([a * b for a, b in contributions]) / sum([a for a, b in contributions])
            Dialgarithm.switch_cache.loc[outgoing.name, victim.name] = weighted_damage
            return weighted_damage

    @staticmethod
    def get_weighted_attack_damage(attacker_name):
        attacker_set = Dialgarithm.moveset_dict[attacker_name]
        if attacker_name in Dialgarithm.attack_cache:
            return Dialgarithm.attack_cache[attacker_name]
        else:
            contributions = [(Dialgarithm.usage_dict[mon.pokemon.unique_name],
                              Damage.deal_damage(attacker_set, mon)) for mon in
                             Dialgarithm.moveset_list]
            weighted_attack = sum([a * b for a, b in contributions])
            Dialgarithm.attack_cache[attacker_name] = weighted_attack
            return weighted_attack

    @staticmethod
    def move_damage(attacker, defender, move):
        if move.name == 'Seismic Toss':
            return 100 / defender.hp_stat
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
        special_factors = coefficient * move.accuracy / 100.0 * 0.925
        damage = (210 / 250 * attacker_atk / defender_def * move.base_power + 2) * special_factors
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
        counters = [m_set for m_set in Dialgarithm.moveset_list if Damage.check_counter(moveset, m_set)]
        return counters
