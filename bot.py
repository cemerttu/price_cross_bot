class PriceCrossBot:
    def __init__(self):
        pass

    def crossing(self, price, level):
        """Check if price == level"""
        return price == level

    def crossing_up(self, prev_price, price, level):
        """Price crosses from below to above level"""
        return prev_price < level <= price

    def crossing_down(self, prev_price, price, level):
        """Price crosses from above to below level"""
        return prev_price > level >= price

    def greater_than(self, price, level):
        return price > level

    def less_than(self, price, level):
        return price < level

    def inside_channel(self, price, lower, upper):
        return lower <= price <= upper

    def outside_channel(self, price, lower, upper):
        return price < lower or price > upper

    def entering_channel(self, prev_price, price, lower, upper):
        """Price moves from outside into the channel"""
        return (prev_price < lower and lower <= price <= upper) or \
               (prev_price > upper and lower <= price <= upper)

    def exiting_channel(self, prev_price, price, lower, upper):
        """Price moves from inside channel to outside"""
        return (lower <= prev_price <= upper) and \
               (price < lower or price > upper)

    def moving_up(self, prev_price, price):
        return price > prev_price

    def moving_down(self, prev_price, price):
        return price < prev_price

    def moving_up_percent(self, prev_price, price):
        if prev_price == 0: 
            return 0
        return ((price - prev_price) / prev_price) * 100 if price > prev_price else 0

    def moving_down_percent(self, prev_price, price):
        if prev_price == 0: 
            return 0
        return ((prev_price - price) / prev_price) * 100 if price < prev_price else 0
