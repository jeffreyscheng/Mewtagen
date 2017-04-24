from Writer import *
import math


class Damage:
    moveset_list = None

    @staticmethod
    def get_moveset_list():
        if Damage.get_moveset_list() is None:
            Damage.moveset_list = [mon for name, mon in Dialgarithm.moveset_dict.items()]
            return Damage.moveset_list
        else:
            return Damage.moveset_list

    @staticmethod
    def read_damage_cache():
        tentative_cache = Writer.load_object('damage.txt')
        if tentative_cache is None:
            Dialgarithm.damage_cache = {}
        else:
            Dialgarithm.damage_cache = tentative_cache

    @staticmethod
    def deal_damage(attacker, defender):
        pair = attacker, defender
        if pair in Dialgarithm.damage_cache:
            return Dialgarithm.damage_cache[pair]
        else:
            damage_list = [Damage.move_damage(attacker, defender, Dialgarithm.dex.move_dict[move])
                           for move in attacker.moves]
            damage = max(damage_list)
            tup = attacker, defender
            Dialgarithm.damage_cache[tup] = damage
            return damage

    @staticmethod
    def get_damage_switch(attacker, switcher, defender):
        pair = attacker, defender
        if pair in Dialgarithm.damage_cache:
            return Dialgarithm.damage_cache[pair]
        else:
            m_dict = Dialgarithm.dex.move_dict
            damage_dict = {m_dict[move]: Damage.move_damage(attacker, defender, m_dict[move])
                           for move in attacker.moves}
            best_move = max(damage_dict, key=damage_dict.get)
            damage = Damage.move_damage(attacker, defender, best_move)
            tup = attacker, switcher, defender
            Dialgarithm.switch_cache[tup] = damage
            return damage

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
            return turns_to_kill_yours < turns_to_kill_theirs - 1

    @staticmethod
    def get_counters_of_moveset(moveset):
        print(moveset.name)
        return [m_set for m_set in Damage.get_moveset_list() if self.check_counter(moveset, m_set)]

    @staticmethod
    def get_all_counters():
        tentative_counters = Writer.load_object('counters.txt')
        if tentative_counters is None:
            Dialgarithm.counters_dict = {moveset: Damage.get_counters_of_moveset(moveset) for moveset in
                                         Damage.get_moveset_list()}
            Writer.save_object(Dialgarithm.counters_dict, 'counters.txt')
        else:
            Dialgarithm.counters_dict = tentative_counters

    @staticmethod
    def get_switches():
        tentative_switches = Writer.load_object('switches.txt')
        if tentative_switches is None:
            Dialgarithm.switch_cache = {}
        else:
            Dialgarithm.switch_cache = tentative_switches
