import os
import pickle
from pathlib import Path
from Dialgarithm import *


class Writer:
    @staticmethod
    def save_object(obj, filename):
        full_filename = Dialgarithm.gen + '/' + filename
        os.makedirs(os.path.dirname(full_filename), exist_ok=True)
        with open(full_filename, 'wb') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_object(filename):
        full_filename = Dialgarithm.gen + '/' + filename
        my_file = Path(full_filename)
        if my_file.is_file():
            return pickle.load(open(full_filename, "rb"))
        else:
            return None
