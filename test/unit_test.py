import unittest


class UnitTests(unittest.TestCase):
    def setUp(self):
        pass

    # sort by id
    def test_sort_by_id(self):
        a = {'id': 10, 'name': 'Anne'}
        b = {'id': 5, 'name': 'Bob'}
        c = {'name': 'Charlie'}

    # TODO test core doesn't change

    # TODO test given core of Gyarados, Mantine, Wingull, pelipper, Swanna -> last one must be ground-type


def main():
    unittest.main()


if __name__ == '__main__':
    main()
