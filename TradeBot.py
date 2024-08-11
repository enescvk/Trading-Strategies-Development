import numpy as np
import pandas as pd
import models as m
import datetime
import sys

df = pd.read_csv("sample.txt", sep = "\t")
df['Timestamp'] = pd.to_datetime(df['Open time'], unit = 'ms')
data = df[['Timestamp', 'Close']]
CPs = [6860, 7400, 8360, 8900, 9950, 10940]

first_model = m.SupportResistanceTradingBot(CPs, 1000)
buy_lines, sell_lines = first_model.create_buy_and_sell_cps(5)
print(data.head(30))

for index, row in data.iterrows():
    if index != 0 and index < 30:
        previous_close = data.loc[index - 1, 'Close']
        first_model.update_prices_and_time(row['Close'], previous_close, row['Timestamp'])
        print(first_model.current_price, first_model.previous_price, first_model.current_time)
"""

support_below, support_above, resistance_below, resistance_above = first_model.get_sup_and_res_lines(5)
print(f"Support Below: {support_below}, Support Above: {support_above}, Resistance Below: {resistance_below}, Resistance Above: {resistance_above}")
"""