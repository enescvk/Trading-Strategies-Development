import pandas as pd
import numpy as np
from datetime import datetime

class SupportResistanceTradingBot():
    def __init__(self, CP_list: list, wallet: float):
        self.CP_list = sorted(CP_list)
        self.wallet = wallet
        self.position_status = None
        self.previous_price = None
        self.current_price = None # Follows the current price to set entry prices when needed.
        self.quantity = 0
        self.transaction_log = []
        self.current_time = None
        self.position_entry_CP = None

    def create_buy_and_sell_cps(self, x):
        self.buy_cps = [i * (100 + x)/100 for i in self.CP_list]
        self.sell_cps = [i * (100 - x)/100 for i in self.CP_list]
        return self.buy_cps, self.sell_cps

    def update_prices_and_time(self, price_cur, price_prev, time_cur):
        # This function updates the price with the current one.
        self.current_price = price_cur
        self.previous_price = price_prev
        self.current_time = time_cur

    def add_cp(self, value: float):
        # This function adds another support or resistance level.
        self.CP_list.append(value)
        self.CP_list.sort()

    def remove_cp(self, value):
        # This function removes a support or resistance level.
        self.CP_list.remove(value)

    def get_sup_and_res_lines(self, x, price): # NEW
        # This function checks price and finds the closest support and resistance level.
        temp_buy_list, temp_sell_list = self.create_buy_and_sell_cps(x)

        temp_buy_list = temp_buy_list + [price]
        temp_buy_list.sort()
        ind_buy = temp_buy_list.index(price)

        temp_sell_list = temp_sell_list + [price]
        temp_sell_list.sort()
        ind_sell = temp_sell_list.index(price)
        #print(ind_buy, ind_sell)

        if ind_buy != 0 or ind_sell != 0 or ind_buy != len(temp_sell_list) - 1 or ind_sell != len(temp_sell_list) - 1:
            return temp_buy_list[ind_buy - 1], temp_buy_list[ind_buy + 1], temp_sell_list[ind_sell - 1], temp_sell_list[ind_sell + 1]
        else:
            raise IndexError("Make sure that the current price is between supports and resistances!")
        
    def log_transaction(self, index, transaction_type):
        # This function logs necessary information whenever there is a new transaction
        transaction = {
            'index': index,
            'type': transaction_type,
            'position_type': self.position_status,
            'price': self.current_price,
            'quantity': self.quantity,
            'wallet_balance': self.wallet,
            'timestamp': self.current_time
        }
        self.transaction_log.append(transaction)

    def determine_action(self, pre_lst, cur_lst):
        if (
            (self.position_status == "short") and 
            (self.position_entry_CP > self.current_price) and
            (self.current_price <= pre_lst[0]) # pre_sup_blw
        ) or (
            (self.position_status == "short") and
            (self.position_entry_CP < self.current_price) and
            (self.current_price >= pre_lst[1]) # pre_sup_abv
            ):
            return "open long"
        
        elif (
            (self.position_status == "long") and
            (self.position_entry_CP > self.current_price) and
            (self.current_price <= pre_lst[2]) # pre_res_blw
        ) or (
            (self.position_status == "long") and 
            (self.position_entry_CP < self.current_price) and
            (self.current_price >= pre_lst[3]) # pre_res_abv
            ):
            return "open short"
        
        elif (
            (self.position_status == None) and
            (self.previous_price > pre_lst[0]) and # pre_sup_blw
            (self.current_price <= cur_lst[1]) and # cur_sup_abv
            (pre_lst[0] == cur_lst[1])
        ) or (
            (self.position_status == None) and
            (self.previous_price < pre_lst[1]) and # pre_sup_abv
            (self.current_price >= cur_lst[0]) and # cur_sup_blw
            (pre_lst[1] == cur_lst[0])
            ):
            return "open long"
        
        elif (
            (self.position_status == None) and
            (self.previous_price > pre_lst[2]) and # pre_res_blw
            (self.current_price <= cur_lst[3]) and # cur_res_abv
            (pre_lst[2] == cur_lst[3])
        ) or (
            (self.position_status == None) and
            (self.previous_price < pre_lst[3]) and # pre_res_blw
            (self.current_price >= cur_lst[2]) and # cur_res_abv
            (pre_lst[3] == cur_lst[2])
        ):
            return "open short"
        
        else:
            return None
        
    def open_long_pos(self, index):
        # Buying logic
        self.position_status = "long"
        self.position_entry_CP = self.current_price
        # Apply changes in the portfolio
        self.quantity = self.wallet / self.current_price  # Calculate quantity
        self.wallet = 0 # Calculate new balance
        self.log_transaction(index, "buy")

    def close_long_pos(self, index): 
        if self.position_status is not None:
            self.wallet = self.quantity * self.current_price
            self.entry_price = None
            self.quantity = 0
            self.position_entry_CP = None
            self.log_transaction(index, "sell")


    def open_short_pos(self, index):
        # Implement short selling logic and log the transaction
        # Buying logic
        self.position_status = "short"
        self.position_entry_CP = self.current_price
        # Apply changes in the portfolio
        self.quantity = -1 * self.wallet / self.current_price  # Calculate quantity
        self.wallet = self.wallet - (self.current_price * self.quantity) # Calculate new balance
        self.log_transaction(index, "sell")

    def close_short_pos(self, index):
        # Implement closing short position logic and log the transaction
        if self.position_status is not None:
            self.wallet = self.wallet + (self.quantity * self.current_price)
            self.entry_price = None
            self.quantity = 0
            self.position_entry_CP = None
            self.log_transaction(index, "buy")

class performance_evaluator():
    def __init__(self, transaction_history: list):
        self.transaction_history = transaction_history

    def overall_performance(self):
        balances = [tr["wallet_balance"] + tr['quantity'] * tr["price"] for tr in self.transaction_history]
        timestamps = [tr["timestamp"] for tr in self.transaction_history]
        time_differences = [(timestamps[i+1] - timestamps[i]).total_seconds() / 3600 for i in range(len(timestamps) - 1)]
        time_diffs_without_zeros = [num for num in time_differences if num != 0]

        self.last_balance = balances[-1]
        self.min_balance = min(balances)
        self.max_balance = max(balances)
        self.trade_amount = len(np.unique(timestamps))
        self.avg_balance = np.average(balances)
        self.min_time_diff = min(time_diffs_without_zeros)
        self.max_time_diff = max(time_diffs_without_zeros)
        self.avg_time_diff = np.average(time_diffs_without_zeros)
        

        return {
                "last_balance": self.last_balance, 
                "min_balance": self.min_balance, 
                "max_balance": self.max_balance,
                "trade_amount": self.trade_amount,
                "avg_balance": self.avg_balance,
                "min_time_diff": self.min_time_diff,
                "max_time_diff": self.max_time_diff,
                "avg_time_diff": self.avg_time_diff
                }

