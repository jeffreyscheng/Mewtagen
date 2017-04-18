from Dex import *


class Dialgarithm:
    link = None
    gen = None
    format = None
    dex = None
    moveset_list = None
    usage_dict = None
    metagame = None
    recommendations = None

    @staticmethod
    def set_link(link):
        Dialgarithm.link = link
        name = link.split('.')[0]
        sections = name.split('-')
        gen_format = sections[0]
        head = gen_format[0:3]
        if head == 'gen':
            index = int(gen_format[3])
            if index == 3:
                Dialgarithm.gen = 'rs'
            elif index == 4:
                Dialgarithm.gen = 'dp'
            elif index == 5:
                Dialgarithm.gen = 'bw'
            elif index == 6:
                Dialgarithm.gen = 'xy'
            elif index == 7:
                Dialgarithm.gen = 'sm'
            else:
                print('invalid gen!')
            Dialgarithm.format = Format(gen_format[4:])
        else:
            Dialgarithm.gen = 'xy'
            Dialgarithm.format = Format(gen_format)
