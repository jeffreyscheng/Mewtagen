from dialgarithm.dialgarithm import *

# import random


def setup():
    UsageReader.select_meta()
    DexFactory().get_dex()
    UsageReader.clean_up_usage()

    # checking megas
    # char_list = MovesetFactory().read_pokemon('Charizard')
    # print([char.name for char in char_list])
    # print([char.pokemon.unique_name for char in char_list])
    # print("done")

    MovesetFactory().get_movesets()
    Damage.read_damage_cache()
    Damage.start()
    # generate normies if necessary
    Metagame.generate_norms()

    tyranitar = Moveset.get_moveset_by_name('Tyranitar_Choice Scarf')
    steelix = Moveset.get_moveset_by_name('Steelix_Tank')
    pidgeot = Moveset.get_moveset_by_name('Pidgeot-Mega_All-out Attacker')

    print(tyranitar == steelix)
    print(tyranitar == tyranitar)

    others = [mon for mon in Model.moveset_list if mon != tyranitar]
    print(tyranitar in others)
    print(len(others))
    print(len(Model.moveset_list))

    # DAMAGE TEST
    # print("DAMAGE TEST:")
    # print("TYRANITAR ON STEELIX")
    # print(Damage.deal_damage(tyranitar, steelix)) # should be 0.45 ish
    # print("TYRANITAR ON PIDGEOT-MEGA")
    # print(Damage.deal_damage(tyranitar, pidgeot)) # should be 1.14 ish

    # COUNTERS TEST
    # print("tyranitar'S COUNTERS:")
    # counters = Damage.get_counters_of_moveset(tyranitar)
    # print([mon.name for mon in counters])
    # print("NOT COUNTERS:")
    # print([mon.name for mon in Model.moveset_list if mon not in counters])

    # TODO: print logs for a single battle


    # MOVESET MUTATION TEST
    for i in range(50):
        newb = tyranitar.mutate()
        print(newb.name)

    # TODO: winning team test -- check overfitting?


def evolve():
    Evolve().evolve()


def output():
    pass

setup()
