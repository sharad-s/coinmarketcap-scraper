'''
#`Horribly unoptimized :'(
#`Quick and dirty.
#``
#`Alt. method is to simply convert
#`the following historical data to a dataframe for analysis:
#`https://www.kaggle.com/jessevent/all-crypto-currencies/version/12
'''
import pandas as pd
import time

#multithreading
import threading

#internal functions and Classes
from listCoins import _listCoins
from scraper import _HTMLTableParser


'''
coin: ["xmr"] or ["xmr", "req", "iota"]
start_date: "YYYYMMDD" - "20130428" or "20180228"
end_date: "YYYYMMDD"

'''
def getCoins(coin = None, limit = None, start_date = None, end_date = None):
    print("Retrieving coin market history from CoinMarketCap.")

    #Get all input coins and build dataframes
    coins = _listCoins(coin, start_date, end_date)           #returns dataframe

    #scrape each url for market data
    scraper = _HTMLTableParser()
    all_dfs = []
    for index, row in coins.iterrows():
        coinnames = row[['slug', 'symbol', 'name', 'rank']]  #Series
        df_names = pd.DataFrame({'slug': [coinnames['slug']],
                            'symbol': [coinnames['symbol']],
                            'name': [coinnames['name']],
                            'rank': [coinnames['rank']]
                            })

        #grab market dataframe from HTML table
        url = row['history_url']
        startTime = time.time()
        df_scraped = scraper.parse_url(url)[0][1]
        print(str(url), 'scraped in', str(time.time() - startTime))

        #repeat names dataframe to match market dataframe
        df_names = pd.concat([df_names]*len(df_scraped.index), ignore_index=True)

        #join names dataframe with market dataframe
        df_joined = pd.concat([df_names,df_scraped], axis=1)

        #append current coin's dataframe to all coins' dataframe
        all_dfs.append(df_joined)

    #stack all dataframes into one df
    df = pd.concat(all_dfs).reset_index(drop=True)

    return df

if __name__ == '__main__':

    #Simple prompt
    print("Enter comma-separated coin symbols.\n(Leave empty to gather all coins)")
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
    # print(df)
    print(type(df), df.shape)

    #outfile
    try:
        df.to_csv("out.csv",index=False, date_format='%Y%m%d')
    except:
        pass
