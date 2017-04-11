from bs4 import BeautifulSoup
import json
import requests
from Moveset import *
from DexFactory import *
from Dialgarithm import *


class MovesetFactory:
    def __init__(self):
        self.dex = Dialgarithm.dex
        self.format = Dialgarithm.format
        self.list_of_movesets = []

    def read_pokemon(self, name):
        moveset_list = []
        # read in json object
        pokemon_url = 'http://www.smogon.com/dex/' + self.dex.gen + '/pokemon/' + name
        soup = BeautifulSoup(requests.get(pokemon_url).text, 'html.parser')
        pokemon_string = soup.script.contents[0]
        pokemon_string = pokemon_string[pokemon_string.find(r'{'):]
        formats = json.loads(pokemon_string)['injectRpcs'][2][1]['strategies']
        for f in formats:
            if f['format'] == self.format:
                movesets = f['movesets']
                moveset_list = [Moveset(self.dex.get_pokemon(name), m_set) for m_set in movesets]
        return moveset_list

    def read_all_movesets(self):
        list_of_pokemon = Dialgarithm.dex.format_metagame.format_dict[Format(Dialgarithm.format)]
        pokemon_names = [pokemon.dex_name for pokemon in list_of_pokemon]
        list_of_moveset_lists = [self.read_pokemon(name) for name in pokemon_names]
        self.list_of_movesets = [m_set for m_list in list_of_moveset_lists for m_set in m_list]
        Dialgarithm.moveset_dict = self.list_of_movesets
