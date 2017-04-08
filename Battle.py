class Battle:
    def __init__(self, metagame):
        self.metagame = metagame
        self.damage_cache = None  # TODO: dict of ordered pairs (attacker, defender) -> damage, read from file

    def battle(self, team1, team2):
        return team1

    def deal_damage(self, attacker, defender):
        return 0

    def move_damage(self, attacker, defender, move):
        return 0
