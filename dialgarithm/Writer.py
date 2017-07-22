import os
import pickle
import pandas as pd
from pathlib import Path
from .model_local import *


class Writer:
    @staticmethod
    def check_path(path):
        if path is None:
            return Model.path
        else:
            return path

    @staticmethod
    def save_pickled_object(obj, filename, path=None):
        path = Writer.check_path(path)
        if not os.path.exists(path):
            os.makedirs(path)
        full_filename = path + filename
        os.makedirs(os.path.dirname(full_filename), exist_ok=True)
        with open(full_filename, 'wb') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        print("WROTE " + filename)

    @staticmethod
    def load_pickled_object(filename, path=None):
        path = Writer.check_path(path)
        full_filename = path + filename
        my_file = Path(full_filename)
        if my_file.is_file():
            return pickle.load(open(full_filename, "rb"))
        else:
            return None

    @staticmethod
    def save_csv_object(obj, filename, path=None):
        print("LOL")
        path = Writer.check_path(path)
        if not os.path.exists(path):
            os.makedirs(path)
        full_filename = path + filename
        os.makedirs(os.path.dirname(full_filename), exist_ok=True)
        obj.to_csv(full_filename)

    @staticmethod
    def load_csv_object(filename, path=None):
        path = Writer.check_path(path)
        full_filename = path + filename
        my_file = Path(full_filename)
        if my_file.is_file():
            return pd.DataFrame.from_csv(my_file)
        else:
            return None

    @staticmethod
    def log(*args):
        message = ' '.join(args) + '\n'
        with open("log.txt", "a") as log_file:
            log_file.write(message)
