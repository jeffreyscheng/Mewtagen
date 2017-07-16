import math
import numpy as np
import time
from .model_local import *


class Moveset:
    mutation_prob = 0.05
    default_ivs = [{'atk': 31, 'def': 31, 'spa': 31,
                    'spd': 31, 'spe': 31, 'hp': 31}]

    def __init__(self, poke, m_set):
        suffix = ''
        if len(m_set['items']) > 0:
            self.item = Model.dex.item_dict[m_set['items'][0]]
            herb = self.item.name != 'White Herb'
            eviolite = self.item.name != 'Eviolite'
            if self.item.name.find('ite') > -1 and herb and eviolite:
                if poke.dex_name in ['Charizard', 'Mewtwo']:
                    if self.item.name.find('X') > -1:
                        suffix = '-Mega-X'
                    else:
                        suffix = '-Mega-Y'
                else:
                    suffix = '-Mega'
        gen = Model.gen
        if len(m_set['natures'][0]) > 0:
            self.nature = Model.dex.get_nature(m_set['natures'][0])
        else:
            self.nature = None
        if len(m_set['ivconfigs']) == 0:
            self.ivs = Moveset.default_ivs
        else:
            self.ivs = m_set['ivconfigs'][0]
        self.evs = m_set['evconfigs'][0]
        self.pokemon = Model.dex.pokemon_dict[poke.unique_name + suffix]
        self.gen = gen
        self.moves = [x[0] if len(x) > 0 else 'Splash'
                      for x in m_set['moveslots']]
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
            nature = 1
        else:
            nature = self.nature.coefficients[name]
        ev_sum = math.floor(ev / 4)
        if name == 'hp':
            return math.floor(2 * base + 31 + ev_sum) + 110
        else:
            return (math.floor(2 * base + 31 + ev_sum) + 5) * nature

    def __hash__(self):
        return hash((self.name, self.pokemon.dex_name, self.gen))

    def __eq__(self, other):
        name = self.name == other.name
        dex = self.pokemon.dex_name == other.pokemon.dex_name
        gen = self.gen == other.gen
        return name and dex and gen

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not self.__eq__(other)

    def mutate(self):
        if np.random.random() < Model.mutation_prob:
            if self in Model.mutation_dict:
                mutation_probability = Model.mutation_dict[self]
            else:
                mutation_probability = self.compute_mutation()
                Model.mutation_dict[self] = mutation_probability
                raise ValueError("Mutations not precomputed?")
            options = [key for key in mutation_probability]
            probabilities = [mutation_probability[key] for key in mutation_probability]

            return np.random.choice(options, p=probabilities)
        else:
            return self

    def compute_mutation(self):
        weights = {mon: Moveset.similarity(self, mon) for mon in Model.moveset_list if mon != self}
        total = np.sum([weights[key] for key in weights])
        return {key: value / total for key, value in weights.items()}

    @staticmethod
    def similarity(moveset1, moveset2):
        # calculate Jaccard index
        min_total = 0
        max_total = 0
        attributes = ['hp_stat', 'atk_stat', 'def_stat', 'spa_stat', 'spd_stat', 'spe_stat']
        for attribute in attributes:
            min_total += min(getattr(moveset1, attribute), getattr(moveset2, attribute))
            max_total += max(getattr(moveset1, attribute), getattr(moveset2, attribute))
        jaccard = min_total
        # calculate type coefficient
        type_coefficient = 0
        for type_key in Model.dex.type_dict:
            move_type = Model.dex.type_dict[type_key]
            type_coefficients1 = np.product([move_type.effects[def_type] for def_type in moveset1.pokemon.types])
            type_coefficients2 = np.product([move_type.effects[def_type] for def_type in moveset2.pokemon.types])
            if type_coefficients1 == type_coefficients2:
                type_coefficient += 1
        type_coefficient /= 18
        return (jaccard ** 7) * (type_coefficient ** 4)

    # FOR TESTING ONLY
    @staticmethod
    def get_moveset_by_name(name):
        return Model.moveset_dict[name]
