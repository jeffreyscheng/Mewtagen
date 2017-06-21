import os
import pickle
import pandas as pd
from pathlib import Path
from Dialgarithm import *


class Writer:
    @staticmethod
    def save_pickled_object(obj, filename):
        if not os.path.exists(Dialgarithm.link):
            os.makedirs(Dialgarithm.link)
        full_filename = Dialgarithm.link + filename
        os.makedirs(os.path.dirname(full_filename), exist_ok=True)
        with open(full_filename, 'wb') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_pickled_object(filename):
        full_filename = Dialgarithm.link + filename
        my_file = Path(full_filename)
        if my_file.is_file():
            return pickle.load(open(full_filename, "rb"))
        else:
            return None

    @staticmethod
    def save_csv_object(obj, filename):
        if not os.path.exists("/" + Dialgarithm.link):
            os.makedirs("/" + Dialgarithm.link)
        full_filename = Dialgarithm.gen + '/' + filename
        os.makedirs(os.path.dirname(full_filename), exist_ok=True)
        obj.to_csv(full_filename)

    @staticmethod
    def load_csv_object(filename):
        full_filename = Dialgarithm.gen + '/' + filename
        my_file = Path(full_filename)
        if my_file.is_file():
            return pd.DataFrame.from_csv(my_file)
        else:
            return None
