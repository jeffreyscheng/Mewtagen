import unittest
from dialgarithm.moveset import *
from dialgarithm.evolve import *


class UnitTests(unittest.TestCase):
    def setUp(self):
        pass

    # sort by id
    def test_mega_altaria(self):
        """ tests that Mega-Altaria's underlying Pokemon is the Mega"""
        altaria = Moveset.get_moveset_by_name('Altaria-Mega_<insert>')
        type_names = [types.name for types in altaria.pokemon.types]
        expected = ['Dragon', 'Fairy']
        union = type_names + expected
        intersection = [types for types in type_names if types not in expected]
        diff = [type_name for type_name in union if type_name not in intersection]
        self.assertEqual(diff, [])

    # TODO test core doesn't change
    def test_core(self):
        pass

    # TODO test given core of Gyarados, Mantine, Wingull, pelipper, Swanna -> last one must be ground-type


def main():
    unittest.main()


if __name__ == '__main__':
    main()
