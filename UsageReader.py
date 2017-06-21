import requests
from bs4 import BeautifulSoup
from Writer import *


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
        print(metagames)
        valid_metagame = False
        while not valid_metagame:
            tentative_link = input("Select a metagame (ex: ou-1825.txt)\n")
            if tentative_link in metagames:
                Dialgarithm.link = tentative_link
                valid_metagame = True
            else:
                print("Not a valid metagame!")

        usage_url += Dialgarithm.link
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
        Dialgarithm.usage_dict = parsed_usage
        Dialgarithm.set_link(Dialgarithm.link)
        print(Dialgarithm.gen)
        Writer.save_pickled_object(parsed_usage, 'usage.txt')