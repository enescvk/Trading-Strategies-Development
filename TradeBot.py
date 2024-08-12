import numpy as np
import pandas as pd
import models as m
import datetime
import sys

df = pd.read_csv("sample.txt", sep = "\t")
df['Timestamp'] = pd.to_datetime(df['Open time'], unit = 'ms')
data = df[['Timestamp', 'Close']]
CPs = [6860, 7400, 8360, 8900, 9950, 10940, 12300]
margin = 2.5

first_model = m.SupportResistanceTradingBot(CPs, 1000)
buy_lines, sell_lines = first_model.create_buy_and_sell_cps(margin)
print(f"Buy Lines: {buy_lines}\nSell Lines: {sell_lines}")

for index, row in data.iterrows():
    if index != 0 and index <= 100000:
        previous_close = data.loc[index - 1, 'Close']
        first_model.update_prices_and_time(row['Close'], previous_close, row['Timestamp'])
        support_below, support_above, resistance_below, resistance_above = first_model.get_sup_and_res_lines(margin)
        if index == 4532 or index == 4531:
            print(index, row['Close'], support_above)
        first_model.open_long_pos(support_below)
        first_model.close_long_pos(resistance_below)
        first_model.open_short_pos(resistance_above)
        first_model.close_short_pos(support_above)

logs = first_model.transaction_log

print(logs)