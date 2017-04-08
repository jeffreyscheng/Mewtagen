from bs4 import BeautifulSoup
import json
import requests
from DexFactory import DexFactory

class MovesetFactory:
    def __init__(self, dex, meta_format):
        self.dex = dex
        self.format = meta_format

    def read_pokemon(self, name):
        # read in json object
        pokemon_url = 'http://www.smogon.com/dex/' + self.dex.gen + '/pokemon/' + name
        soup = BeautifulSoup(requests.get(pokemon_url).text, 'html.parser')
        pokemon_string = soup.script.contents[0]
        pokemon_string = pokemon_string[pokemon_string.find(r'{'):]
        formats = json.loads(pokemon_string)['injectRpcs'][2][1]['strategies']
        for f in formats:
            if f['format'] == self.format:
                movesets = f['movesets']
                for m_set in movesets:
                    print(m_set)
                    # parse this out
                    # m_name = self.get_unique_name(name, m_set['items'])
                    # m_set['unique_name'] = m_name
                    # self.moveset_list.append(m_set)
        return None

    def read_all_movesets(self):
        return None

with open('lol.txt', 'w+') as output:
    output.write('lol')
xy_dex = DexFactory().get_dex('bw') #  TODO: debug this shite
mf = MovesetFactory(xy_dex, 'OU')
mf.read_pokemon('Charizard')