class Dex:
    def __init__(self, gen, pokemon_list, move_list, type_list, nature_list, item_list)
        self.gen = gen
        self.pokemon_list = pokemon_list
        self.move_list = move_list
        self.type_list = type_list
        self.nature_list = nature_list
        self.item_list = item_list


class Pokemon:
    def __init__(self, properties):
        self.unique_name = properties['name'] + properties['suffix']
        self.dex_name = properties['name']
        self.base_hp = properties['hp']
        self.base_atk = properties['atk']
        self.base_def = properties['def']
        self.base_sp_atk = properties['spa']
        self.base_sp_def = properties['spd']
        self.base_spe = properties['spe']
        self.formats = properties['formats']


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
        self.atk_coefficient = properties['atk']
        self.def_coefficient = properties['def']
        self.spa_coefficient = properties['spa']
        self.spd_coefficient = properties['spd']
        self.dpe_coefficient = properties['spe']


class Item:
    def __init__(self, properties):
        self.name = properties['name']
        self.description = properties['description']
