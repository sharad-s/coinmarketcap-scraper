import requests
import pandas as pd
import json
from pandas.io.json import json_normalize
import datetime

quick_search_url = "https://files.coinmarketcap.com/generated/search/quick_search.json"


'''
Pass in coins as array
coins = ['xmr']
'''

def listCoins(coins = None, start_date = None, end_date = None):

    #set start_date, end_date
    if not start_date:
        start_date = "20130428"
    if not end_date:
        end_date = str(datetime.date.today()).replace('-','')

    #Get all coins from URL and convert to Dataframe
    r = requests.get(quick_search_url)
    if (r.status_code == 200):
        a = json.loads(r.text)
        res = json_normalize(a)
        df = pd.DataFrame(res)


    #grab Columns from dataframe
    # id = df[df.columns[0]]
    # name = df[df.columns[1]]
    # rank = df[df.columns[2]]
    # slug = df[df.columns[3]]
    # symbol = df[df.columns[4]]
    all_coins = df[df.columns[5]]

    #Grab indices of input coins from dataframe
    #Searches for symbol, slug, or name
    #TODO: optimize search
    indices = []
    if coins:
        for k, entry in enumerate(all_coins):
            for coin in coins:
                if coin in entry or coin.upper() in entry:
                    indices.append(k)

    #If no input coins, use all rows from dataframe
    else:
        indices = list(range(len(df.index)))

    #Create subset dataframe
    df_subset = df.loc[indices, ['symbol', 'name', 'slug', 'rank']]

    #add exchange url and history url to subset
    exchange_urls = []
    history_urls = []
    for index, row in df_subset.iterrows():
        exchange_urls.append("https://coinmarketcap.com/currencies/" + str(row['slug']) + "/#markets")
        history_urls.append("https://coinmarketcap.com/currencies/" + str(row['slug']) + "/historical-data/?start=" + str(start_date) + "&end=" + str(end_date))
    df_subset['exchange_url'] = exchange_urls
    df_subset['history_url'] = history_urls

    #Return Subset
    # pd.options.display.max_colwidth = 100
    # print(df_subset['history_url'])
    return df_subset

if __name__ == '__main__':
    df = listCoins(['litecoin','xrp', 'iota'])
    print(df)
