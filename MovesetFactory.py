from Moveset import *
from DexFactory import *
from Dialgarithm import *


class MovesetFactory:
    def __init__(self):
        self.dex = Dialgarithm.dex
        self.format = Dialgarithm.format

    def read_pokemon(self, name):
        moveset_list = []
        # read in json object
        pokemon_url = 'http://www.smogon.com/dex/' + self.dex.gen + '/pokemon/' + name
        soup = BeautifulSoup(requests.get(pokemon_url).text, 'html.parser')
        pokemon_string = soup.script.contents[0]
        pokemon_string = pokemon_string[pokemon_string.find(r'{'):]
        formats = json.loads(pokemon_string)['injectRpcs'][2][1]['strategies']
        for f in formats:
            if Format(f['format']) <= self.format:
                movesets = f['movesets']
                moveset_list = [Moveset(self.dex.get_pokemon(name), m_set) for m_set in movesets]
        print('Read: ' + name)
        return moveset_list

    def get_movesets(self):
        tentative_movesets = Writer.load_object('movesets.txt')
        if tentative_movesets is None:
            format_dict = Dialgarithm.dex.format_metagame.format_dict
            meta_format = Dialgarithm.format
            list_of_pokemon = [format_dict[Format(form)] for form in Format.format_list
                               if Format(form) <= meta_format]
            list_of_pokemon = [pokemon for mini_list in list_of_pokemon for pokemon in mini_list]
            pokemon_to_moveset = {pokemon.unique_name: self.read_pokemon(pokemon.dex_name)
                                  for pokemon in list_of_pokemon}

            def attach_usage(moveset, usage):
                moveset.usage = usage
                return moveset

            def add_usage(pokemon):
                if pokemon.unique_name not in Dialgarithm.usage_dict.keys():
                    print('NOT FOUND')
                    print(pokemon.unique_name)
                    return []
                else:
                    usage = Dialgarithm.usage_dict[pokemon.unique_name]
                    options = pokemon_to_moveset[pokemon.unique_name]
                    print([attach_usage(moveset, usage / len(options)) for moveset in options])
                    return [attach_usage(moveset, usage / len(options)) for moveset in options]

            nested_list = [add_usage(pokemon) for pokemon in list_of_pokemon]
            Dialgarithm.moveset_dict = {m_set.name: m_set for m_sets in nested_list for m_set in m_sets}
            Writer.save_object(Dialgarithm.moveset_dict, 'movesets.txt')
        else:
            Dialgarithm.moveset_dict = tentative_movesets
        Dialgarithm.moveset_list = [value for key, value in Dialgarithm.moveset_dict.items()]
