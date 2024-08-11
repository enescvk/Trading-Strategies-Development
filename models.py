import pandas as pd

class SupportResistanceTradingBot():
    def __init__(self, CP_list: list, wallet: float):
        self.CP_list = sorted(CP_list)
        self.wallet = wallet
        self.position_status = None
        self.entry_price = None # Indicates the entry price of the positions.
        self.previous_price = None
        self.current_price = None # Follows the current price to set entry prices when needed.
        self.quantity = 0
        self.transaction_log = []
        self.current_time = None

    def create_buy_and_sell_cps(self, x):
        self.buy_cps = [i * (100 + x)/100 for i in self.CP_list]
        self.sell_cps = [i * (100 - x)/100 for i in self.CP_list]
        return self.buy_cps, self.sell_cps

    def update_prices_and_time(self, price_cur, price_prev, time_cur):
        # This function updates the price with the current one.
        self.current_price = price_cur
        self.previous_price = price_prev
        self.current_time = time_cur

    def add_cl(self, value: float):
        # This function adds another support or resistance level.
        self.CP_list.append(value)
        self.CP_list.sort()

    def remove_cl(self, value):
        # This function removes a support or resistance level.
        self.CP_list.remove(value)

    def get_sup_and_res_lines(self, x): # NEW
        # This function checks price and finds the closest support and resistance level.
        temp_buy_list, temp_sell_list = self.create_buy_and_sell_cps(x)

        temp_buy_list = temp_buy_list + [self.current_price]
        temp_buy_list.sort()
        ind_buy = temp_buy_list.index(self.current_price)

        temp_sell_list = temp_sell_list + [self.current_price]
        temp_sell_list.sort()
        ind_sell = temp_sell_list.index(self.current_price)

        if ind_buy != 0 or ind_sell != 0 or ind_buy != len(temp_sell_list) - 1 or ind_sell != len(temp_sell_list) - 1:
            return temp_buy_list[ind_buy - 1], temp_buy_list[ind_buy + 1], temp_sell_list[ind_sell - 1], temp_sell_list[ind_sell + 1]
        else:
            raise ValueError("Make sure that the current price is between supports and resistances!")
        
    def log_transaction(self, time, transaction_type, position_type, price, quantity): # NEW
        # This function logs necessary information whenever there is a new transaction
        transaction = {
            'type': transaction_type,
            'position_type': position_type,
            'price': price,
            'quantity': quantity,
            'wallet_balance': self.wallet,
            'timestamp': time
        }
        self.transaction_log.append(transaction)

    def open_long_pos(self, sup_blw): # NEW
        if (self.position_status is None) and (self.wallet > 0) and (self.previous_price >= sup_blw) and (self.current_price <= sup_blw):
            # Buying logic
            self.position_status = "long"
            self.entry_price = self.current_price
            # Apply changes in the portfolio
            self.quantity = self.wallet / self.current_price  # Calculate quantity
            self.wallet = self.wallet - (self.current_price * self.quantity) # Calculate new balance
            self.log_transaction("buy", self.current_time, self.position_status, self.current_price, self.quantity)

    def close_long_pos(self, res_blw): # NEW
        if (self.position_status == "long") and (self.previous_price >= res_blw) and (self.current_price <= res_blw):
            self.wallet += self.quantity * self.current_price
            self.log_transaction("sell", self.current_time, self.position_status, self.current_price, self.quantity)
            self.position_status = None
            self.entry_price = None
            self.quantity = 0

    def open_short_pos(self, res_above): # NEW
        # Implement short selling logic and log the transaction
        if (self.position_status is None) and (self.wallet > 0) and (self.previous_price <= res_above) and (self.current_price >= res_above):
            # Buying logic
            self.position_status = "short"
            self.entry_price = self.current_price
            # Apply changes in the portfolio
            self.quantity = -1 * self.wallet / self.current_price  # Calculate quantity
            self.wallet = self.wallet - (self.current_price * self.quantity) # Calculate new balance
            self.log_transaction("sell", self.current_time, self.position_status, self.current_price, self.quantity)

    def close_short_pos(self, sup_above): # NEW
        # Implement closing short position logic and log the transaction
        if (self.position_status == "short") and (self.previous_price <= sup_above) and (self.current_price >= sup_above):
            self.wallet += -1 * self.quantity * self.current_price
            self.log_transaction("sell", self.current_time, self.position_status, self.current_price, self.quantity)
            self.position_status = None
            self.entry_price = None
            self.quantity = 0


