class Dex:
    def __init__(self, gen, pokemon_dict, move_list, type_list, nature_dict, item_list):
        self.gen = gen
        self.pokemon_dict = pokemon_dict
        self.move_list = move_list
        self.type_list = type_list
        self.nature_dict = nature_dict
        self.item_list = item_list

    def get_pokemon(self, name):
        return self.pokemon_dict[name]

    def get_nature(self, name):
        return self.nature_dict[name]


class Pokemon:
    def __init__(self, properties):
        self.unique_name = properties['name'] + properties['suffix']
        self.dex_name = properties['name']
        self.base_hp = properties['hp']
        self.base_atk = properties['atk']
        self.base_def = properties['def']
        self.base_spa = properties['spa']
        self.base_spd = properties['spd']
        self.base_spe = properties['spe']
        self.formats = properties['formats']

    def get_base_stat(self, name):
        return self.__dict__['base_' + name]


class Move:
    def __init__(self, properties):
        self.name = properties['name']
        self.base_power = properties['power']
        self.accuracy = properties['accuracy']
        self.category = properties['category']


class Type:
    def __init__(self, name, atk_effective):
        self.name = name
        self.atk_dict = atk_effective

    def type_coefficient(self, def_type):
        return self.atk_dict[def_type]


class Nature:
    def __init__(self, properties):
        self.name = properties['name']
        self.coefficients = properties


class Item:
    def __init__(self, properties):
        self.name = properties['name']
        self.description = properties['description']
