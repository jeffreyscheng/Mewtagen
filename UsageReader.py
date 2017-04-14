import requests
from bs4 import BeautifulSoup


class UsageReader:

    @staticmethod
    def get_usage():
        pass

    @staticmethod
    def get_usage_from_date(date_string):
        # parse Dialgarithm.link
        date_string = '2017-02'
        usage_url = 'http://www.smogon.com/stats/' + date_string + '/' + Dialgarithm.link
        soup = BeautifulSoup(requests.get(usage_url).text, 'html.parser')
        usage_string = soup.text
        usage_rows = usage_string.split('\n')
        usage_rows = usage_rows[5:len(usage_rows) - 2]
        parsed_usage = [row.split('|') for row in usage_rows]

        def strip_row(row):
            return list(filter(None, [element.strip('%\n\t\r ') for element in row]))
        parsed_usage = [strip_row(row) for row in parsed_usage]
        parsed_usage = {row[1]: float(row[2]) / 600 for row in parsed_usage}
        return parsed_usage