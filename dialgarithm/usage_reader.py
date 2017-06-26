import requests
from bs4 import BeautifulSoup
from .model_local import *
from .view import *
from .Writer import *


class UsageReader:
    # gets most recent date and prints metagames
    @staticmethod
    def select_meta():
        # gets most recent date
        usage_url = 'http://www.smogon.com/stats/'
        soup = BeautifulSoup(requests.get(usage_url).text, 'html.parser')
        tags = soup('a')
        date_string = tags[-1]['href']

        # prints all metagames
        usage_url += date_string
        soup = BeautifulSoup(requests.get(usage_url).text, 'html.parser')
        tags = soup('a')
        not_metagames = ['../', 'chaos/', 'leads/', 'mega/', 'metagame/', 'monotype/', 'moveset/']
        metagames = [tag['href'] for tag in tags if tag['href'] not in not_metagames]
        Message.message(str(metagames))

        def condition(user_input):
            return user_input in metagames

        tentative_link = Prompt.prompt("Select a metagame (ex: ou-1825.txt)\n", condition)
        Model.link = tentative_link
        # save usage_url into db?
        usage_url += Model.link
        soup = BeautifulSoup(requests.get(usage_url).text, 'html.parser')
        usage_string = soup.text
        usage_rows = usage_string.split('\n')
        usage_rows = usage_rows[5:len(usage_rows) - 2]
        parsed_usage = [row.split('|') for row in usage_rows]

        def strip_row(row):
            return list(filter(None, [element.strip('%\n\t\r ') for element in row]))

        parsed_usage = [strip_row(row) for row in parsed_usage]
        parsed_usage = {row[1]: float(row[2]) / 600
                        for row in parsed_usage}
        Model.usage_dict = parsed_usage
        Model.set_link(Model.link)
        # save json-pickled object to firebase
        Writer.save_pickled_object(parsed_usage, 'usage.txt')

    @staticmethod
    def clean_up_usage():
        usage_dict = Model.usage_dict
        other_mons = [mon for mon in Model.dex.pokemon_dict.keys() if mon not in usage_dict.keys()]
        zeros = {mon: 0 for mon in other_mons}
        Model.usage_dict = {**usage_dict, **zeros}