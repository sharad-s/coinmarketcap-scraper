import requests
import pandas as pd
import json
import datetime
import requests

#parallel processing
from pathos.parallel import ParallelPool as ParallelPool

from pandas.io.json import json_normalize
from listCoins import listCoins
from scraper import scraper, HTMLTableParser

'''
coin: "xrp" or ["xrp", "req", "iota"]
limit: ""
'''

def getCoins(coin = None, limit = None, cpu_cores = None, start_date = None, end_date = None):
    print("Retrieves coin market history from CoinMarketCap.")

    #Get all input coins and build dataframes
    coins = listCoins(coin, start_date, end_date)
    coinnames = coins[['symbol', 'name', 'rank', 'slug']]

    # pd.options.display.max_colwidth = 100

    #Obtain all urls
    history_urls = []
    for index, url in coins['history_url'].iteritems():
        history_urls.append(url)

    #TODO: Can only Scrape one coin at the moment
    scraper = HTMLTableParser()
    df = scraper.parse_url(history_urls[0])

    # return df
    return df

if __name__ == '__main__':
    df = getCoins(['xmr', 'xrp', 'neo'])
    print(df)
