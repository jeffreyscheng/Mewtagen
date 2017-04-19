import numpy as np


class Team:
    def __init__(self, list_of_movesets):
        self.list_of_movesets = list_of_movesets

    def is_valid(self):
        list_of_names = [m_set.pokemon.dex_name for m_set in self.list_of_movesets]
        return np.unique(list_of_names).size == len(list_of_names)
