class Dex:
    def __init__(self, gen, pokemon_dict, move_dict,
                 type_dict, nature_dict, item_dict):
        self.gen = gen
        self.pokemon_dict = pokemon_dict
        self.move_dict = move_dict
        self.type_dict = type_dict
        self.nature_dict = nature_dict
        self.item_dict = item_dict
        self.format_metagame = FormatMetagame([self.pokemon_dict[key]
                                               for key in self.pokemon_dict])

    def get_pokemon(self, name):
        return self.pokemon_dict[name]

    def get_nature(self, name):
        return self.nature_dict[name]


class Pokemon:
    def __init__(self, properties):
        suffix = ''
        if properties['suffix'] is not None:
            if len(properties['suffix']) > 0:
                suffix = '-' + properties['suffix']
        self.unique_name = properties['name'] + suffix
        self.dex_name = properties['name']
        self.base_hp = properties['hp']
        self.base_atk = properties['atk']
        self.base_def = properties['def']
        self.base_spa = properties['spa']
        self.base_spd = properties['spd']
        self.base_spe = properties['spe']
        self.formats = properties['formats']
        self.types = properties['types']

    def get_base_stat(self, name):
        return self.__dict__['base_' + name]


class Move:
    def __init__(self, properties):
        self.name = properties['name']
        self.base_power = properties['power']
        self.accuracy = properties['accuracy']
        self.category = properties['category']
        self.type = properties['type']


class Type:
    def __init__(self, name, atk_effective):
        self.name = name
        self.effects = atk_effective


class Nature:
    def __init__(self, properties):
        self.name = properties['name']
        self.coefficients = properties


class Item:
    def __init__(self, properties):
        self.name = properties['name']
        self.description = properties['description']


class Format:
    format_list = ['LC', 'PU', 'BL4', 'NU',
                   'BL3', 'RU', 'BL2', 'UU',
                   'BL', 'OU', 'Uber', 'AG']

    def __init__(self, form_string):
        format_string = form_string.upper()
        self.name = format_string
        if format_string == 'LC':
            self.rank = -1
        elif format_string == 'PU':
            self.rank = 0
        elif format_string == 'BL4':
            self.rank = 1
        elif format_string == 'NU':
            self.rank = 2
        elif format_string == 'BL3':
            self.rank = 3
        elif format_string == 'RU':
            self.rank = 4
        elif format_string == 'BL2':
            self.rank = 5
        elif format_string == 'UU':
            self.rank = 6
        elif format_string == 'BL':
            self.rank = 7
        elif format_string == 'OU':
            self.rank = 8
        elif format_string == 'UBER':
            self.rank = 9
        elif format_string == 'AG' or format_string == 'Limbo':
            self.rank = 10
        else:
            self.rank = 11

    def __lt__(self, other):
        return self.rank < other.rank

    def __le__(self, other):
        return self.rank <= other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def __ge__(self, other):
        return self.rank >= other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __hash__(self, ):
        return hash(self.rank)


class FormatMetagame:
    def __init__(self, list_of_pokemon):
        self.format_dict = {}
        for pokemon in list_of_pokemon:
            self.append_pokemon(pokemon)

    def append_pokemon(self, pokemon):
        for meta_format in pokemon.formats:
            f = Format(meta_format)
            if f in self.format_dict.keys():
                self.format_dict[f].append(pokemon)
            else:
                self.format_dict[f] = [pokemon]
