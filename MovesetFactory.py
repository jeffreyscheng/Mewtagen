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

    def get_movesets(self):
        tentative_movesets = Writer.load_object('movesets.txt')
        if tentative_movesets is None:
            format_dict = Dialgarithm.dex.format_metagame.format_dict
            meta_format = Dialgarithm.format
            list_of_pokemon = [format_dict[Format(form)] for form in Format.format_list
                               if form <= meta_format]
            list_of_pokemon = [pokemon for mini_list in list_of_pokemon for pokemon in mini_list]
            pokemon_names = [pokemon.dex_name for pokemon in list_of_pokemon]
            list_of_moveset_lists = [self.read_pokemon(name) for name in pokemon_names]
            self.list_of_movesets = [m_set for m_list in list_of_moveset_lists for m_set in m_list]
            Writer.save_object(self.list_of_movesets, 'movesets.txt')
        else:
            self.list_of_movesets = tentative_movesets
        Dialgarithm.moveset_dict = self.list_of_movesets
