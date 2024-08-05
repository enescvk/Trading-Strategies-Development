class SupportResistanceTradingBot():
    def __init__(self, entry_price: float):
        self.entry_price = entry_price
        self.price = []
        self.position = None

    def update_price(self, price: float):
        """Update the bot with the latest price."""
        self.prices.append(price)
        if len(self.prices) > 5:
            self.prices.pop(0)  # Maintain only the necessary history

    #def compare_price_and_lines(self, )

