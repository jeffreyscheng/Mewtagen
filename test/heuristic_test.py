from dialgarithm.dialgarithm import *

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

    tyranitar = Moveset.get_moveset_by_name('Tyranitar_Choice Scarf')

    # DAMAGE TEST
    print("DAMAGE TEST:")
    steelix = Moveset.get_moveset_by_name('Steelix_Tank')
    lilligant = Moveset.get_moveset_by_name('Lilligant_Quiver Dance')
    print("TYRANITAR ON STEELIX")
    print(Damage.deal_damage(tyranitar, steelix))
    print("TYRANITAR ON LILLIGANT")
    print(Damage.deal_damage(tyranitar, lilligant))

    # COUNTERS TEST
    print("tyranitar'S COUNTERS:")
    print([mon.name for mon in Model.counters_dict[tyranitar]])
    print("NOT COUNTERS:")
    print([mon.name for mon in Model.moveset_list if mon not in Model.counters_dict[tyranitar]])


    # MOVESET MUTATION TEST
    print([mon.name for mon in Model.moveset_list])
    for i in range(50):
        tyranitar.mutate()
        print(tyranitar.name)


def evolve():
    Evolve().evolve()


def output():
    pass
