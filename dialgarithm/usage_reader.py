import requests
from bs4 import BeautifulSoup
from .model_local import *
import os
from .view import *
from .Writer import *


class UsageReader:
    updating = True

    # TODO: GET METAS FUNCTIOn FOR PRECOMPUTATION


    @staticmethod
    def assign_meta():
        # gets most recent date
        # usage_url = 'http://www.smogon.com/stats/'
        # soup = BeautifulSoup(requests.get(usage_url).text, 'html.parser')
        # tags = soup('a')
        # date_string = tags[-1]['href']
        # Model.date = date_string
        #
        # usage_url += date_string
        # soup = BeautifulSoup(requests.get(usage_url).text, 'html.parser')
        # tags = soup('a')
        # not_metagames = ['../', 'chaos/', 'leads/', 'mega/', 'metagame/', 'monotype/', 'moveset/']
        # metagames = [tag['href'] for tag in tags if tag['href'] not in not_metagames]
        Model.date = "2017-06/"
        Model.set_link("ou-1825.txt")
        Model.set_path()

        # initializes date if necessary
        # needs_update = not os.path.isdir("./" + date_string)
        # if needs_update and UsageReader.updating:
        # UsageReader.initialize_date(metagames)
        # else:
        Model.usage_dict = Writer.load_pickled_object('usage.txt', Model.path)

    # gets most recent date and prints metagames
    @staticmethod
    def select_meta():
        # gets most recent date
        usage_url = 'http://www.smogon.com/stats/'
        soup = BeautifulSoup(requests.get(usage_url).text, 'html.parser')
        tags = soup('a')
        date_string = tags[-1]['href']

        ## TODO: FIX DATES
        date_string = '2017-06/'
        Model.date = date_string

        usage_url += date_string
        soup = BeautifulSoup(requests.get(usage_url).text, 'html.parser')
        tags = soup('a')
        not_metagames = ['../', 'chaos/', 'leads/', 'mega/', 'metagame/', 'monotype/', 'moveset/']
        metagames = [tag['href'] for tag in tags if tag['href'] not in not_metagames]

        def condition(user_input):
            return user_input in metagames

        Message.message(str(metagames))
        Model.set_link(Prompt.prompt("Select a metagame (ex: ou-1825.txt)\n", condition))
        Model.set_path()

        # initializes date if necessary
        needs_update = not os.path.isdir("./" + date_string)
        if needs_update and UsageReader.updating:
            UsageReader.initialize_date(metagames)
        else:
            Model.usage_dict = Writer.load_pickled_object('usage.txt', Model.path)

    @staticmethod
    def initialize_date(list_of_metas):
        os.makedirs("./" + Model.date)
        for meta in list_of_metas:
            UsageReader.initialize_meta(meta)

    @staticmethod
    def initialize_meta(meta):
        print("initializing " + meta)
        stripped_meta = meta.split(".")[0]
        os.makedirs("./" + Model.date + "/" + stripped_meta)
        usage_url = 'http://www.smogon.com/stats/' + Model.date + "/" + meta
        soup = BeautifulSoup(requests.get(usage_url).text, 'html.parser')
        usage_string = soup.text
        usage_rows = usage_string.split('\n')
        usage_rows = usage_rows[5:len(usage_rows) - 2]
        parsed_usage = [row.split('|') for row in usage_rows]

        def strip_row(row):
            return list(filter(None, [element.strip('%\n\t\r ') for element in row]))

        parsed_usage = [strip_row(row) for row in parsed_usage]
        if len(parsed_usage) == 0:
            Model.usage_dict = {}
        elif len(parsed_usage) == 1 and not parsed_usage[0]:
            Model.usage_dict = {}
        else:
            parsed_usage = {row[1]: float(row[2]) / 600
                            for row in parsed_usage}
            Model.usage_dict = parsed_usage
        Writer.save_pickled_object(parsed_usage, 'usage.txt', "./" + Model.date + "/" + stripped_meta + "/")

    @staticmethod
    def clean_up_usage():
        other_mons = [mon for mon in Model.dex.pokemon_dict.keys() if mon not in Model.usage_dict.keys()]
        zeros = {mon: 0 for mon in other_mons}
        Model.usage_dict = {**Model.usage_dict, **zeros}