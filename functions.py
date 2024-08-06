class SupportResistanceTradingBot():
    def __init__(self, list_of_lines: list):
        self.list_of_lines = sorted(list_of_lines)

    def add_support_or_resistance(self, value: float):
        self.list_of_lines.append(value)
        self.list_of_lines.sort()

    def remove_support_or_resistance(self, value: float):
        self.list_of_lines.remove(value)

    def compare_price_and_lines(self, price):
        temp_list = self.list_of_lines + [price]
        temp_list.sort()
        ind = temp_list.index(price)
        return temp_list[ind - 1], temp_list[ind + 1]

first_model = SupportResistanceTradingBot([5, 10, 20, 40])
first_model.add_support_or_resistance(15.5)
first_model.remove_support_or_resistance(10)
lower, upper = first_model.compare_price_and_lines(17)

print(lower, upper)

