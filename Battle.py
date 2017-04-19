from Dialgarithm import *
import random


class Battle:
    def __init__(self):
        self.metagame = Dialgarithm.metagame
        self.damage_cache = None  # TODO: dict of ordered pairs (attacker, defender) -> damage, read from file

    def battle(self, team1, team2):
        return random.choice([team1, team2])

    def deal_damage(self, attacker, defender):


    def move_damage(self, attacker, defender, move):
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
        damage = (210 / 250 * attacker_atk / defender_def * move.base_power + 2) * coefficient * move.accuracy / 100.0 * 0.925
        if damage >= defender.hp_stat:
            return 1
        else:
            return damage / defender.hp_stat
