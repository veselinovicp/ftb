import json
from urllib.parse import quote
import configparser
import pandas as pd
import requests


class DataMachine:
    def __init__(self, currency="EUR_USD", number_of_samples=1000):

        self.currency = currency
        self.number_of_samples = number_of_samples


        self.profit = 0.0020
        self.loss = 0.0020
        self.train_percent = 70.
        self.input_labels = []

    def prepare_data(self):
        self.__download_data()
        self.__prepare_data()
        self.__prepare_windowed_data()

        self.__prepare_test_and_train()

    def __prepare_test_and_train(self):


        split_num = int(self.train_percent/100. * len(self.df))
        print("split_num: ", split_num)

        train = self.df[:split_num]
        test = self.df[split_num:]

        output_labels = ['buy', 'sell', 'idle']

        train_input = train[self.input_labels]
        train_output = train[output_labels]

        test_input = test[self.input_labels]
        test_output = test[output_labels]

        train_input.to_csv("../data/" + self.currency + "_train_input.csv")
        train_output.to_csv("../data/" + self.currency + "_train_output.csv")

        test_input.to_csv("../data/" + self.currency + "_test_input.csv")
        test_output.to_csv("../data/" + self.currency + "_test_output.csv")


    def __prepare_windowed_data(self):
        print("preparing data")
        # df = pd.read_csv('data/EUR_USD_200000_prepared.csv', float_precision='round_trip')
        print("data length: ", len(self.df))

        for s in range(1, 129):

            bid___format = 'openBid_{}'.format(s)
            self.input_labels.append(bid___format)
            self.df[bid___format] = self.df['openBid'].shift(s)

            ask___format = 'openAsk_{}'.format(s)
            self.input_labels.append(ask___format)
            self.df[ask___format] = self.df['openAsk'].shift(s)

            high_bid___format = 'highBid_{}'.format(s)
            self.input_labels.append(high_bid___format)
            self.df[high_bid___format] = self.df['highBid'].shift(s)

            high_ask___format = 'highAsk_{}'.format(s)
            self.input_labels.append(high_ask___format)
            self.df[high_ask___format] = self.df['highAsk'].shift(s)

            low_bid___format = 'lowBid_{}'.format(s)
            self.input_labels.append(low_bid___format)
            self.df[low_bid___format] = self.df['lowBid'].shift(s)

            low_ask___format = 'lowAsk_{}'.format(s)
            self.input_labels.append(low_ask___format)
            self.df[low_ask___format] = self.df['lowAsk'].shift(s)

            close_bid___format = 'closeBid_{}'.format(s)
            self.df[close_bid___format] = self.df['closeBid'].shift(s)
            self.input_labels.append(close_bid___format)

            close_ask___format = 'closeAsk_{}'.format(s)
            self.df[close_ask___format] = self.df['closeAsk'].shift(s)
            self.input_labels.append(close_ask___format)

            volume___format = 'volume_{}'.format(s)
            self.df[volume___format] = self.df['volume'].shift(s)
            self.input_labels.append(volume___format)
        self.df.dropna(axis=0, inplace=True)

    def __should_sell(self, index, openBid):
        for i in range(index, min(index + 33, len(self.df))):
            if (self.df.at[i, 'highAsk'] - openBid > self.loss):
                print("(should_sell) high ask at: ", i, " is: ", self.df.at[i, 'highAsk'], ", which is more than: ", self.loss,
                      " more open bid: ", openBid, " at index: ", index, " WONT BUY")
                return False
            if (openBid - self.df.at[i, 'lowAsk'] > self.profit):
                print("(should_sell) low ask at: ", i, " is: ", self.df.at[i, 'lowAsk'], ", which is less than: ", self.profit,
                      " more open bid: ",
                      openBid, " at index: ", index, " WILL BUY")
                return True

        return False

    def __should_buy(self, index, openAsk):

        for i in range(index, min(index + 33, len(self.df))):
            if (openAsk - self.df.at[i, 'lowBid'] > self.loss):
                print("(should_buy) low bid at: ", i, " is: ", self.df.at[i, 'lowBid'], ", which is more than: ", self.loss,
                      " less open ask: ", openAsk, " at index: ", index, " WONT BUY")
                return False
            if (self.df.at[i, 'highBid'] - openAsk > self.profit):
                print("(should_buy) high bid at: ", i, " is: ", self.df.at[i, 'highBid'], ", which is more than: ", self.profit,
                      " more open ask: ",
                      openAsk, " at index: ", index, " WILL BUY")
                return True

        return False

    def __prepare_data(self):
        print("preparing data")

        # self.df = pd.read_csv('data/EUR_USD_200000.csv', float_precision='round_trip')
        print("data length: ", len(self.df))
        new_columns = pd.DataFrame([], columns=["buy", "sell", "idle"])
        self.df = self.df.join(new_columns)

        # df['0', 'buy'] = 1

        i = 0
        for index, row in self.df.iterrows():
            print(index, ", row: ", row['openBid'])

            if self.__should_buy(index, row['openAsk']):
                self.df.set_value(index, 'buy', 1)
                self.df.set_value(index, 'sell', 0)
                self.df.set_value(index, 'idle', 0)
            elif self.__should_sell(index, row['openBid']):
                self.df.set_value(index, 'buy', 0)
                self.df.set_value(index, 'sell', 1)
                self.df.set_value(index, 'idle', 0)
            else:
                self.df.set_value(index, 'buy', 0)
                self.df.set_value(index, 'sell', 0)
                self.df.set_value(index, 'idle', 1)

            i = i + 1
            # if i > 500:
            #     break

        # df.to_csv("data/EUR_USD_200000_prepared.csv")

    def __download_data(self):
        config = configparser.RawConfigParser()
        config.read('../secret.properties')

        tokenValue = config.get('DEFAULT', 'OANDA_API_KEY')
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
                url = "https://api-fxtrade.oanda.com/v1/candles?instrument=" + self.currency + "&count=" + str(
                    candlesPerDownload) + "&candleFormat=bidask&granularity=M1&dailyAlignment=0&alignmentTimezone=Europe%2FLjubljana"  # &alignmentTimezone=Europe\/Ljubljana
            else:
                url = "https://api-fxtrade.oanda.com/v1/candles?instrument=" + self.currency + "&count=" + \
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

            for i, val in enumerate(resp['candles']):  # reversed  enumerate
                combined.append(val)

            if totalAmount >= self.number_of_samples:
                # with open("data/EUR_USD_" + str(totalAmount) + ".json", 'w') as outfile:
                #     json.dump(combined, outfile)
                headers = ["time", "openBid", "openAsk", "highBid", "highAsk", "lowBid", "lowAsk", "closeBid",
                           "closeAsk", "volume"]
                self.df = pd.DataFrame(combined, columns=headers)

                self.df['time'] = pd.to_datetime(self.df['time'])
                self.df = self.df.sort_values(by=['time'])
                self.df = self.df.drop_duplicates()

                self.df.reset_index(drop=True, inplace=True)
                # self.df = self.df.sort_values(by=['time'])

                # self.df.index = self.df['time']
                # del self.df['time']
                # self.df.sort_index(inplace=True)



                    # df.to_csv("data/EUR_USD_" + str(totalAmount) + ".csv")
                break

            totalAmount += candlesPerDownload

            i = i + 1
