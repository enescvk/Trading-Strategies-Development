import numpy as np
import pandas as pd
import models as m
import datetime
import sys

df = pd.read_csv("sample.txt", sep = "\t")
df['Timestamp'] = pd.to_datetime(df['Open time'], unit = 'ms')
data = df[['Timestamp', 'Close']]
CPs = [6860, 7400, 8360, 8900, 9950, 10940]

first_model = m.SupportResistanceTradingBot(data.Timestamp, data.Close, CPs, 1000)
print(first_model.current_time, first_model.current_price, first_model.CP_list, first_model.wallet)
"""
buy_lines, sell_lines = first_model.create_buy_and_sell_cps(5)
print(f"Buy Lines: {buy_lines}\nSell Lines: {sell_lines}")
first_model.add_cl(15.0)
first_model.remove_cl(10.0)
buy_lines, sell_lines = first_model.create_buy_and_sell_cps(5)
print(f"New Buy Lines: {buy_lines}\nNew Sell Lines: {sell_lines}")
first_model.update_prices_and_time(30, 33)
support_below, support_above, resistance_below, resistance_above = first_model.get_sup_and_res_lines(5)
print(f"Support Below: {support_below}, Support Above: {support_above}, Resistance Below: {resistance_below}, Resistance Above: {resistance_above}")
"""