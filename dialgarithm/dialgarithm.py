# from .model_local import Model
from .usage_reader import *
from .dex_factory import DexFactory
from .moveset_factory import MovesetFactory
# import random


def setup():
    UsageReader.select_meta()
    DexFactory().get_dex()
    UsageReader.clean_up_usage()
    MovesetFactory().get_movesets()
    print('LOL')


def evolve():
    pass


def output():
    pass
