'''
#' historical table scraper
#' This web scrapes the historic price tables from CoinMarketCap
#' and provides back a dataframe for the coin provided as an input.
#' This function is a dependency of getCoins and is used
#' as part of a loop to retrieve all crypto currencies.
'''
import pandas as pd
from bs4 import BeautifulSoup
import requests

class HTMLTableParser:

    def parse_url(self, url):
        r = requests.get(url)
        html_string = str(r.content)
        soup = BeautifulSoup(html_string, 'lxml')
        return [(table['class'],self.parse_html_table(table)) for table in soup.find_all('table')]

    def parse_html_table(self, table):
        n_columns = 0
        n_rows=0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,
                          index= range(0,n_rows))
        row_marker = 0
        # print(table.find_all('tr')[::-1])

        for row in table.find_all('tr')[::-1]:
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1

        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass

        return df


def scraper(history_url):
    r = requests.get(history_url)
    html_string = str(r.content)
    soup = BeautifulSoup(html_string, 'lxml')
    table = soup.find_all('table')[0] # Grab the first table
    print ([(table['class']) for table in soup.find_all('table')])

if __name__ == '__main__':
    history_url = 'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=20180226'
    scraper = HTMLTableParser()
    df = scraper.parse_url(history_url)
    print(df)
