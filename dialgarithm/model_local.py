from .dex import *


class Model:
    core = []
    link = None
    gen = None
    format = None
    dex = None
    moveset_dict = None
    moveset_list = None
    usage_dict = None
    counters_dict = None
    damage_cache = None
    attack_cache = None
    switch_cache = {}
    metagame = None
    recommendations = None
    population_size = 0
    time = 0

    @staticmethod
    def set_link(link):
        Model.link = link
        name = link.split('.')[0]
        sections = name.split('-')
        gen_format = sections[0]
        head = gen_format[0:3]
        if head == 'gen':
            index = int(gen_format[3])
            if index == 3:
                Model.gen = 'rs'
            elif index == 4:
                Model.gen = 'dp'
            elif index == 5:
                Model.gen = 'bw'
            elif index == 6:
                Model.gen = 'xy'
            elif index == 7:
                Model.gen = 'sm'
            else:
                print('invalid gen!')
            Model.format = Format(gen_format[4:])
        else:
            Model.gen = 'xy'
            Model.format = Format(gen_format)
        Model.link = name + "/"
