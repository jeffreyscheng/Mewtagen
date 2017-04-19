import numpy as np


class Team:
    def __init__(self, list_of_movesets):
        self.party = {moveset: 1 for moveset in list_of_movesets}
        self.current = None

    def is_valid(self):
        list_of_names = [m_set.pokemon.dex_name for m_set in self.party.keys()]
        return np.unique(list_of_names).size == len(list_of_names)

    def heal(self):
        self.party = {moveset: 1 for moveset in self.party.keys()}
        self.current = None
