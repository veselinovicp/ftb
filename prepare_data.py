
import pandas as pd

profit = 0.0020
loss = 0.0020

def should_sell(index, openBid, df):
    for i in range(index, min(index+33, len(df))):
        if(df.at[i, 'highAsk'] - openBid > loss):
            print("(should_sell) high ask at: ", i, " is: ", df.at[i, 'highAsk'],", which is more than: ", loss, " more open bid: ", openBid, " at index: ", index, " WONT BUY")
            return False
        if (openBid - df.at[i, 'lowAsk'] > profit):
            print("(should_sell) low ask at: ", i, " is: ", df.at[i, 'lowAsk'], ", which is less than: ", profit, " more open bid: ",
                  openBid, " at index: ", index, " WILL BUY")
            return True

    return False

def should_buy(index, openAsk, df):
    for i in range(index, min(index+33, len(df))):
        if(openAsk - df.at[i, 'lowBid'] > loss):
            print("(should_buy) low bid at: ", i, " is: ", df.at[i, 'lowBid'],", which is more than: ", loss, " less open ask: ", openAsk, " at index: ", index, " WONT BUY")
            return False
        if (df.at[i, 'highBid'] - openAsk > profit):
            print("(should_buy) high bid at: ", i, " is: ", df.at[i, 'highBid'], ", which is more than: ", profit, " more open ask: ",
                  openAsk," at index: ",index, " WILL BUY")
            return True

    return False

def prepare_data():
    print("preparing data")
    df = pd.read_csv('data/EUR_USD_200000.csv', float_precision='round_trip')
    print("data length: ", len(df))
    new_columns = pd.DataFrame([], columns=["buy", "sell", "idle"])
    df = df.join(new_columns)

    # df['0', 'buy'] = 1

    i = 0
    for index, row in df.iterrows():
        print(index, ", row: ", row['openBid'])

        if should_buy(index, row['openAsk'], df):
            df.set_value(index, 'buy', 1)
            df.set_value(index, 'sell', 0)
            df.set_value(index, 'idle', 0)
        elif should_sell(index, row['openBid'], df):
            df.set_value(index, 'buy', 0)
            df.set_value(index, 'sell', 1)
            df.set_value(index, 'idle', 0)
        else:
            df.set_value(index, 'buy', 0)
            df.set_value(index, 'sell', 0)
            df.set_value(index, 'idle', 1)




        i = i + 1
        # if i > 500:
        #     break


    df.to_csv("data/EUR_USD_200000_prepared.csv")










def main():
    prepare_data()


##################################
###           MAIN           ####
##################################

if __name__ == "__main__": main()