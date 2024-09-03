import numpy as np
import pandas as pd
import models as m
import datetime
import sys

df = pd.read_csv("sample.txt", sep = "\t")
df['Timestamp'] = pd.to_datetime(df['Open time'], unit = 'ms')
data = df[['Timestamp', 'Close']]


# SUPPORT RESISTANCE BOT
CPs = [6860, 7400, 8360, 8900, 9950, 10940, 12300]
support_resistance_margin = 0.499
first_model = m.SupportResistanceTradingBot(CP_list = CPs, wallet = 1000)
buy_lines, sell_lines = first_model.create_buy_and_sell_cps(support_resistance_margin)
print(f"Buy Lines: {buy_lines}\nSell Lines: {sell_lines}")

for index, row in data.iterrows():
    if index != 0 and index < 5:
        previous_close = data.loc[index - 1, 'Close']
        first_model.update_prices_and_time(row['Close'], previous_close, row['Timestamp'])
        cur_pr_lines = list(first_model.get_sup_and_res_lines(support_resistance_margin, first_model.current_price))
        prev_pr_lines = list(first_model.get_sup_and_res_lines(support_resistance_margin, first_model.previous_price))
        print(first_model.position_entry_CP, first_model.determine_action(prev_pr_lines, cur_pr_lines))

        if first_model.determine_action(prev_pr_lines, cur_pr_lines) == "open long":
            first_model.close_short_pos(index)
            first_model.open_long_pos(index)
            #print(f"index: {index}\nPrev_price: {first_model.previous_price}\nCur_price: {first_model.current_price}\nPre_sup_blw: {prev_pr_lines[0]}\nPre_sup_abv: {prev_pr_lines[1]}\nCur_sup_blw: {cur_pr_lines[0]}\nCur_sup_abv: {cur_pr_lines[1]}\n----------")
        elif first_model.determine_action(prev_pr_lines, cur_pr_lines) == "open short":
            first_model.close_long_pos(index)
            first_model.open_short_pos(index)
        else:
            continue

logs = first_model.transaction_log

performance = m.performance_evaluator(logs)
result_dict = performance.overall_performance()
print(result_dict)


