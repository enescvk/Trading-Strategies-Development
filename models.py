import pandas as pd

class SupportResistanceTradingBot():
    def __init__(self, df, list_of_lines: list, wallet: float):
        self.list_of_lines = sorted(list_of_lines)
        self.wallet = wallet
        self.df = df
        self.position_status = None
        self.entry_price = None # Indicates the entry price of the positions.
        self.previous_price = None
        self.current_price = None # Follows the current price to set entry prices when needed.
        self.quantity = 0
        self.transaction_log = []

    def update_prices(self, price_cur, price_prev): # NEW
        # This function updates the price with the current one.
        self.current_price = price_cur
        self.previous_price = price_prev

    def add_support_or_resistance(self, value: float):
        # This function adds another support or resistance level.
        self.list_of_lines.append(value)
        self.list_of_lines.sort()

    def remove_support_or_resistance(self, value: float):
        # This function removes a support or resistance level.
        self.list_of_lines.remove(value)

    def check_price_and_lines(self):
        # This function checks price and finds the closest support and resistance level.
        temp_list = self.list_of_lines + [self.current_price]
        temp_list.sort()
        ind = temp_list.index(self.current_price)
        if ind != 0:
            return temp_list[ind - 1], temp_list[ind + 1]
        else:
            raise ValueError("There is no lower support level than the price! You have to add a lower support level!")
        
    def log_transaction(self, transaction_type, position_type, price, quantity): # NEW
        transaction = {
            'type': transaction_type,
            'position_type': position_type,
            'price': price,
            'quantity': quantity,
            'wallet_balance': self.wallet,
            'timestamp': pd.Timestamp.now()
        }
        self.transaction_log.append(transaction)

    def open_long_pos(self): # NEW
        #lower, upper = self.check_price_and_lines(self.current_price)
        if (self.position_status is None) and (self.wallet > 0):
            # Buying logic
            self.position_status = "long"
            self.entry_price = self.current_price
            # Apply changes in the portfolio
            self.quantity = self.wallet / self.current_price  # Calculate quantity
            self.wallet = self.wallet - (self.current_price * self.quantity) # Calculate new balance
            self.log_transaction("buy", self.position_status, self.current_price, self.quantity)

    def close_long_pos(self): # NEW
        #lower, upper = self.check_price_and_lines(self.current_price)
        if self.position_status == "long":
            self.wallet += self.quantity * self.current_price
            self.log_transaction("sell", self.position_status, self.current_price, self.quantity)
            self.position_status = None
            self.entry_price = None
            self.quantity = 0

    def open_short_pos(self): # NEW
        # Implement short selling logic and log the transaction
        #lower, upper = self.check_price_and_lines(self.current_price)
        if (self.position_status is None):
            # Buying logic
            self.position_status = "short"
            self.entry_price = self.current_price
            # Apply changes in the portfolio
            self.quantity = -1 * self.wallet / self.current_price  # Calculate quantity
            self.wallet = self.wallet - (self.current_price * self.quantity) # Calculate new balance
            self.log_transaction("sell", self.position_status, self.current_price, self.quantity)

    def close_short_pos(self): # NEW
        # Implement closing short position logic and log the transaction
        #lower, upper = self.check_price_and_lines(self.current_price)
        if self.position_status == "short":
            self.wallet += -1 * self.quantity * self.current_price
            self.log_transaction("sell", self.position_status, self.current_price, self.quantity)
            self.position_status = None
            self.entry_price = None
            self.quantity = 0

            

first_model = SupportResistanceTradingBot([5, 10, 20, 40])
first_model.add_support_or_resistance(15.5)
first_model.remove_support_or_resistance(10)
lower, upper = first_model.check_price_and_lines(4)

print(lower, upper)
