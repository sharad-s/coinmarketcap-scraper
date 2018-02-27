'''
Horribly unoptimized :'(
Quick and dirty.


Alt. method is to simply convert
the following historical data to a dataframe for analysis:
https://www.kaggle.com/jessevent/all-crypto-currencies/version/12
'''
import pandas as pd
import time
import pprint

#multithreading
import threading

#internal functions and Classes
from listCoins import _listCoins
from scraper import _HTMLTableParser


'''
coin: ["xmr"] or ["xmr", "req", "iota"]
limit: "" #not implemented yet
'''
def getCoins(coin = None, limit = None, start_date = None, end_date = None):
    print("Retrieving coin market history from CoinMarketCap.")

    #Get all input coins and build dataframes
    coins = _listCoins(coin, start_date, end_date)               #returns dataframe
    df_coinnames = coins[['symbol', 'name', 'rank', 'slug']]       #dataframe

    #Obtain all urls
    history_urls = []
    for index, url in coins['history_url'].iteritems():
        history_urls.append(url)

    #scrape each url for market data
    scraper = _HTMLTableParser()
    all_dfs = []
    for url in history_urls:

        #grab market dataframe from HTML table
        startTime = time.time()
        df_scraped = scraper.parse_url(url)[0][1]
        print(str(url), 'scraped in', str(time.time() - startTime))

        all_dfs.append(df_scraped)


    #stack all dataframes into one df
    df = pd.concat(all_dfs).reset_index(drop=True)


    #TODO: ADD NAMES TO DATAFRAME! By..
    #TODO: join scraped dataframe with respective coinname data
    #>for url in history_urls:
    #>   get df_scraped

    #>   for row in df_coinnames which contains 'symbol':
    #>       add row of df_coinnames to all rows of df_scraped

    #>stack all dataframes into one df
    #>return df

    return df

if __name__ == '__main__':

    #Simple prompt, not necessary
    print("Enter comma-separated coin symbols.\nLeave empty to collect all coins")
    print('Example: "xmr, neo, iota, req"')
    coins = input('>')
    if not coins:
        coins = None
    else:
        try:
            coins = coins.replace(" ","").split(",")
        except:

            coins = coins.replace(" ","")


    #run getCoins
    df = getCoins(coins)
    print(df)
    print(type(df), df.shape)

    #out
    try:
        df.to_csv("out.csv", sep='\t')
    except:
        pass
