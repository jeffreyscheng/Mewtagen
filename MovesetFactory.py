from bs4 import BeautifulSoup
import json
import requests
from Moveset import Moveset
from DexFactory import DexFactory


class MovesetFactory:
    def __init__(self, dex, meta_format):
        self.dex = dex
        self.format = meta_format
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
                moveset_list = [Moveset(self.dex.get_pokemon(name), self.format, m_set) for m_set in movesets]
        return moveset_list

    def read_all_movesets(self):
        list_of_moveset_lists = [read_pokemon(name) for name in self.dex.pokemon_dict.keys()]
        self.list_of_movesets = [m_set for m_list in list_of_moveset_lists for m_set in m_list]


# if run normally -> permission error 13
# if run from Pycharm in admin mode -> can read + write to 'ghost' files?
# if run from commandline -> works perfectly but can't find Pycharm's written files?

with open('lol.txt', 'w+') as output:
    print('gotcha')
    output.write('incredible')

# with open('lol.txt', 'r') as input:
#     print(input.read())

# xy_dex = DexFactory().get_dex('bw')  # TODO: debug this shite
# mf = MovesetFactory(xy_dex, 'OU')
# mf.read_pokemon('Charizard')
