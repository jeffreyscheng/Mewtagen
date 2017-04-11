from Dialgarithm import *
from DexFactory import *
from MovesetFactory import *
from MetagameFactory import *

# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def index():
#     return "homepage"
#
#
# if __name__ == '__main__'"":
#     app.run()

Dialgarithm.set_meta('xy', 'OU')
DexFactory().set_dex()
mf = MovesetFactory()
mf.read_pokemon('Charizard')
