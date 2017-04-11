from Writer import *
from DexFactory import *


class Dialgarithm:
    gen = None
    format = None
    dex = None
    moveset_dict = None  # -> usage statistics
    metagame = None
    recommendations = None

    @staticmethod
    def set_meta(gen, meta_format):
        Dialgarithm.gen = gen
        Dialgarithm.format = meta_format

    @staticmethod
    def initialize_dex():
        tentative_dex = Writer.load_object(Dialgarithm.gen + '_dex.txt')
        if tentative_dex is None:
            Dialgarithm.dex = DexFactory().get_dex()
            # Writer.save_object(Dialgarithm.dex, Dialgarithm.gen + '_dex.txt')
        else:
            Dialgarithm.dex = tentative_dex

    @staticmethod
    def initialize_meta():
        pass
