import json
import requests
from bs4 import BeautifulSoup
from .model_local import *
from .Writer import *


class DexFactory:
    def __init__(self):
        self.gen = None
        self.raw_dex = None
        self.type_dict = None
        self.pokemon_dict = None
        self.nature_dict = None
        self.move_dict = None
        self.item_dict = None

    def get_dex(self):
        tentative_dex = Writer.load_pickled_object('dex.txt')
        if tentative_dex is None:
            self.gen = Model.gen
            self.read_dex()
            self.read_types()
            self.read_pokemon()
            self.read_natures()
            self.read_moves()
            self.read_items()
            new_dex = Dex(self.gen, self.pokemon_dict, self.move_dict,
                          self.type_dict, self.nature_dict, self.item_dict)
            Writer.save_pickled_object(new_dex, 'dex.txt')
        else:
            new_dex = tentative_dex
        Model.dex = new_dex

    @staticmethod
    def unwrap(old_dict, col):
        def flatten_alt(alt):
            new_dict = old_dict.copy()
            for stat in alt.keys():
                new_dict[stat] = alt[stat]
            del new_dict[col]
            return new_dict

        alt_list = list(old_dict[col])
        list_of_dicts = [flatten_alt(alt) for alt in alt_list]
        return list_of_dicts

    def read_dex(self):
        dex_url = 'http://www.smogon.com/dex/' + self.gen + '/pokemon/'
        soup = BeautifulSoup(requests.get(dex_url).text, 'html.parser')
        dex_string = soup.script.contents[0]
        dex_string = dex_string[dex_string.find(r'{'):]
        self.raw_dex = json.loads(dex_string)['injectRpcs'][1][1]
        print(self.raw_dex['pokemon'])

    def read_types(self):

        def extract_type(type_dict):
            atk_effective = {}
            for response_type in type_dict['atk_effectives']:
                atk_effective[response_type[0]] = response_type[1]
            return Type(type_dict['name'], atk_effective)

        type_list = [extract_type(type_dict) for type_dict
                     in self.raw_dex['types']]
        self.type_dict = {t.name: t for t in type_list}

    def read_pokemon(self):
        alt_list = [DexFactory.unwrap(poke, 'alts') for poke
                    in self.raw_dex['pokemon']]
        alt_list = [alt for sublist in alt_list for alt in sublist]
        pokemon_list = [Pokemon(alt) for alt in alt_list]
        self.pokemon_dict = {poke.unique_name: poke for poke in pokemon_list}

    def read_natures(self):
        self.nature_dict = {nature['name']: Nature(nature) for nature
                            in self.raw_dex['natures']}

    def read_moves(self):
        self.move_dict = {move['name']: Move(move) for move
                          in self.raw_dex['moves']}

    def read_items(self):
        self.item_dict = {item['name']: Item(item) for item
                          in self.raw_dex['items']}
