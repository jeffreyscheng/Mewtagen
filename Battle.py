from Dialgarithm import *


class Battle:
    def __init__(self):
        self.metagame = Dialgarithm.metagame
        self.damage_cache = None  # TODO: dict of ordered pairs (attacker, defender) -> damage, read from file
        # create a folder for each gen
        # refactor load from Writer
        # each folder has xy_dex, xy_movesets, xy_damage_cache

    def battle(self, team1, team2):
        return team1

    def deal_damage(self, attacker, defender):
        return 0

    def move_damage(self, attacker, defender, move):
        return 0
