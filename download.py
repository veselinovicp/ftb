# !/usr/bin/python
import subprocess, os, csv
import json, httplib2, math, calendar, datetime, requests
from time import *
import pandas as pd
import sys
import json
from urllib.parse import quote

# https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count=2&candleFormat=bidask&granularity=D&dailyAlignment=0&alignmentTimezone=America%2FNew_York

global OandaSymbol
OandaSymbol = {
    'EURUSD': 'EUR_USD',
    'GBPUSD': 'GBP_USD',
    'USDJPY': 'USD_JPY',
    'AUDUSD': 'AUD_USD',
    'USDCHF': 'USD_CHF',
    'USDCAD': 'USD_CAD',
    'EURCHF': 'EUR_CHF',
    'EURGBP': 'EUR_GBP',
    'EURJPY': 'EUR_JPY',
    'AUDJPY': 'AUD_JPY',
    'AUDCAD': 'AUD_CAD',
    'GBPJPY': 'GBP_JPY',
    'GBPCHF': 'GBP_CHF',
    'GBPAUD': 'GBP_AUD',
    'GBPCAD': 'GBP_CAD',
    'EURAUD': 'EUR_AUD',
    'EURCAD': 'EUR_CAD',
    'CHFJPY': 'CHF_JPY',
    'CADJPY': 'CAD_JPY'
}


def update_positioning_data(tokenValue, count):
    token = "Bearer %s" % (tokenValue)

    headers = {'Authorization': token, 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip, deflate',
               'Content-type': 'application/x-www-form-urlencoded'}

    global OandaSymbol

    i = 0

    totalAmount = 0

    start = ""

    end = ""

    combined = []

    while True:

        candlesPerDownload = 5000

        if i == 0:
            url = "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count=" + str(
                candlesPerDownload) + "&candleFormat=bidask&granularity=M1&dailyAlignment=0&alignmentTimezone=Europe%2FLjubljana"  # &alignmentTimezone=Europe\/Ljubljana
        else:
            url = "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count=" + \
                  str(candlesPerDownload) + \
                  "&candleFormat=bidask&granularity=M1&dailyAlignment=0&alignmentTimezone=Europe%2FLjubljana&end=" + end  # +"&includeFirst=false"

        resp = {}

        try:
            req = requests.get(url, headers=headers)
            resp = req.json()
        except Exception:
            e = Exception
            print("ERROR GETTING DATA. ABORTING.")
            quit()


        start_temp = resp['candles'][candlesPerDownload - 1]['time']
        start = quote(resp['candles'][candlesPerDownload - 1]['time'])

        end_temp = resp['candles'][0]['time']
        end = quote(resp['candles'][2]['time'])
        print("start: ", start_temp, ", end: " + end_temp)

        for i, val in enumerate(resp['candles']):   #reversed  enumerate
            combined.append(val)



        if totalAmount >= count:
            with open("EUR_USD_" + str(totalAmount) + ".json", 'w') as outfile:

                json.dump(combined, outfile)
                headers = ["time", "openBid", "openAsk", "highBid", "highAsk", "lowBid", "lowAsk", "closeBid", "closeAsk", "volume"]
                df = pd.DataFrame(combined, columns=headers)

                df['time'] = pd.to_datetime(df['time'])
                df = df.drop_duplicates()

                df.index = df['time']


                del df['time']
                df.sort_index(inplace=True)



                df.to_csv("EUR_USD_" + str(totalAmount) + ".csv")#, date_format='%Y-%m-%d %H:%M:%S'
            break

        totalAmount += candlesPerDownload

        i = i + 1

    # position_data = resp['data'][OandaSymbol[symbol]]['data']
    # for p in range(len(position_data)):
    #     position_data[p][0] = datetime.datetime.fromtimestamp(position_data[p][0])
    # headers = ["timestamp", "lpr", "rate"]
    # df = pd.DataFrame(position_data, columns=headers)
    # df = df.set_index(df['timestamp'])
    # df = df.drop(['timestamp', 'rate'], axis=1)
    # df = df[:-1]
    #
    # try:
    #     old_df = pd.DataFrame.from_csv("OANDA_POSITION_"+symbol + '.csv', index_col=0)
    #     df = pd.concat([df,old_df])
    # except:
    #     print
    #     'No old datafile found. Generating new one.'
    #
    # df = df[~df.index.duplicated(keep='first')]
    #
    # df.to_csv("OANDA_POSITION_"+symbol + '.csv', date_format='%Y-%m-%d %H:%M:%S')


def main():
    symbolsToUpdate = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "EURJPY", "AUDUSD", "AUDJPY", "EURAUD", "USDCAD",
                       "GBPJPY", "EURGBP", "GBPCHF", "CADJPY"]

    update_positioning_data("SECRET_KEY", 200000)


##################################
###           MAIN           ####
##################################

if __name__ == "__main__": main()
