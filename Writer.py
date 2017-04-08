import pickle
from pathlib import Path


class Writer:
    @staticmethod
    def save_object(obj, filename):
        with open(filename, 'w+') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_object(filename):
        my_file = Path(filename)
        if my_file.is_file():
            return pickle.load(open(filename, "rb"))
        else:
            return None
