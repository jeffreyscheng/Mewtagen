from .moveset import *
from .dex_factory import *
from .model_local import *
from time import sleep


class MovesetFactory:
    def __init__(self):
        self.dex = Model.dex
        self.format = Model.format

    def read_pokemon(self, name):
        try:
            # read in json object
            pokemon_url = 'http://www.smogon.com/dex/' + self.dex.gen + \
                          '/pokemon/' + name
            soup = BeautifulSoup(requests.get(pokemon_url).text, 'html.parser')
            pokemon_string = soup.script.contents[0]
            pokemon_string = pokemon_string[pokemon_string.find(r'{'):]
            formats = json.loads(pokemon_string)['injectRpcs'][2][1]['strategies']
            moveset_list = []
            for f in formats:
                if Format(f['format']) <= self.format:
                    movesets = f['movesets']
                    moveset_list += [Moveset(self.dex.get_pokemon(name), m_set) for m_set in movesets]
            print('Read: ' + name)
            return moveset_list
        except requests.exceptions.ConnectionError:
            print("CONNECTION DENIED ON " + name, ", RETRYING")
            sleep(30)
            self.read_pokemon(name)

    def get_movesets(self):
        tentative_movesets = Writer.load_pickled_object('movesets.txt')
        if tentative_movesets is None:
            format_dict = Model.dex.format_metagame.format_dict
            meta_format = Model.format
            list_of_pokemon = [format_dict[Format(form)] for form
                               in Format.format_list
                               if Format(form) <= meta_format]
            list_of_pokemon = [pokemon for mini_list in list_of_pokemon
                               for pokemon in mini_list]
            pokemon_to_moveset =\
                {pokemon.unique_name: self.read_pokemon(pokemon.dex_name)
                 for pokemon in list_of_pokemon}

            def attach_usage(moveset, usage):
                moveset.usage = usage
                return moveset

            def add_usage(pokemon):
                if pokemon.unique_name not in Model.usage_dict.keys():
                    print('NOT FOUND')
                    print(pokemon.unique_name)
                    return []
                else:
                    usage = Model.usage_dict[pokemon.unique_name]
                    options = pokemon_to_moveset[pokemon.unique_name]
                    if options is None:
                        return []
                    else:
                        return [attach_usage(moveset, usage / len(options))
                                for moveset in options]

            nested_list = [add_usage(pokemon) for pokemon in list_of_pokemon]
            Model.moveset_dict = {m_set.name: m_set for m_sets in nested_list for m_set in m_sets}
            Writer.save_pickled_object(Model.moveset_dict,
                                       'movesets.txt')
        else:
            Model.moveset_dict = tentative_movesets
        Model.moveset_list = [value for key, value
                                    in Model.moveset_dict.items()]
