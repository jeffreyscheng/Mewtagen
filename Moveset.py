import math
from Dialgarithm import *


class Moveset:
    default_ivs = [{'atk': 31, 'def': 31, 'spa': 31, 'spd': 31, 'spe': 31, 'hp': 31}]

    def __init__(self, poke, m_set):
        gen = Dialgarithm.gen
        if len(m_set['natures'][0]) > 0:
            self.nature = Dialgarithm.dex.get_nature(m_set['natures'][0])
        else:
            self.nature = None
        if len(m_set['ivconfigs']) == 0:
            self.ivs = Moveset.default_ivs
        else:
            self.ivs = m_set['ivconfigs'][0]
        self.evs = m_set['evconfigs'][0]
        self.pokemon = poke
        self.gen = gen
        self.moves = [x[0] if len(x) > 0 else 'Splash' for x in m_set['moveslots']]
        self.hp_stat = self.get_stat('hp')
        self.atk_stat = self.get_stat('atk')
        self.def_stat = self.get_stat('def')
        self.spa_stat = self.get_stat('spa')
        self.spd_stat = self.get_stat('spd')
        self.spe_stat = self.get_stat('spe')
        self.usage = 0
        self.name = self.pokemon.unique_name + '_' + m_set['name']

    def get_stat(self, name):
        base = self.pokemon.get_base_stat(name)
        ev = self.evs[name]
        if self.nature is None:
            nature_coefficient = 1
        else:
            nature_coefficient = self.nature.coefficients[name]
        if name == 'hp':
            return math.floor(2 * base + 31 + math.floor(ev / 4)) + 110
        else:
            return (math.floor(2 * base + 31 + math.floor(ev / 4)) + 5) * nature_coefficient

    def __hash__(self):
        return hash((self.name, self.pokemon.dex_name, self.gen))

    def __eq__(self, other):
        return self.name == other.name and self.pokemon.dex_name == other.pokemon.dex_name and self.gen == other.gen

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)
