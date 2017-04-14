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
        # self.cardinality_dict = None

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
        self.get_usage()
        tentative_movesets = Writer.load_object('movesets.txt')
        # cardinality_dict = Writer.load_object('cardinality.txt')
        if tentative_movesets is None:
            format_dict = Dialgarithm.dex.format_metagame.format_dict
            meta_format = Dialgarithm.format
            list_of_pokemon = [format_dict[Format(form)] for form in Format.format_list
                               if form <= meta_format]
            list_of_pokemon = [pokemon for mini_list in list_of_pokemon for pokemon in mini_list]
            pokemon_names = [pokemon.dex_name for pokemon in list_of_pokemon]
            pokemon_to_moveset = {name: self.read_pokemon(name) for name in pokemon_names}
            nested_list = [self.get_usage(key, value) for key, value in pokemon_to_moveset.items()]
            self.list_of_movesets = [m_set for m_sets in nested_list for m_set in m_sets]
            Writer.save_object(self.list_of_movesets, 'movesets.txt')
            Dialgarithm.moveset_dict = self.list_of_movesets
        else:
            self.list_of_movesets = tentative_movesets
        Dialgarithm.moveset_dict = self.list_of_movesets

    def get_usage(self):
        # parse Dialgarithm.link
        usage_url = 'http://www.smogon.com/stats/2017-02/' + Dialgarithm.link
        print(usage_url)
        soup = BeautifulSoup(requests.get(usage_url).text, 'html.parser')
        usage_string = soup.text
        usage_rows = usage_string.split('\n')
        usage_rows = usage_rows[5:len(usage_rows) - 2]
        parsed_usage = [row.split('|') for row in usage_rows]

        def strip_row(row):
            return [element.strip() for element in row]
        parsed_usage = [strip_row(row) for row in parsed_usage]
        parsed_usage = list(filter(None, parsed_usage))
        print(parsed_usage)
        parsed_usage = {row[1]: row[2] for row in parsed_usage}
        print(parsed_usage)
        return 0
        # get usage of pokemon
        # divide by len(value of dict)
        # assign to each pkmn
        # return list of movesets