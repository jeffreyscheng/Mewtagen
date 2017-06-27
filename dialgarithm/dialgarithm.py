# from .model_local import Model
from .usage_reader import *
from .dex_factory import DexFactory
from .moveset_factory import MovesetFactory
from .damage import *
from .metagame import *
from .evolve import *


# import random


def setup():
    UsageReader.select_meta()
    DexFactory().get_dex()
    UsageReader.clean_up_usage()
    MovesetFactory().get_movesets()
    Damage.read_damage_cache()
    Damage.get_switches()
    Damage.get_all_counters()
    # generate normies if necessary
    Metagame.generate_norms()


# def evolve():
#     Evolve().evolve()


def output():
    pass
