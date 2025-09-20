from bot import PriceCrossBot

class SimpleStrategy:
    def __init__(self, level=1.10, lower=1.09, upper=1.11):
        self.bot = PriceCrossBot()
        self.level = level
        self.lower = lower
        self.upper = upper
        self.position = None  # "LONG", "SHORT", or None

    def on_price(self, prev_price, price):
        """Run strategy on each new price tick."""

        signals = []

        # Example entry rules
        if self.bot.crossing_up(prev_price, price, self.level):
            if self.position != "LONG":
                self.position = "LONG"
                signals.append(f"🟢 BUY at {price}")

        if self.bot.crossing_down(prev_price, price, self.level):
            if self.position != "SHORT":
                self.position = "SHORT"
                signals.append(f"🔴 SELL at {price}")

        # Example exit rules
        if self.bot.exiting_channel(prev_price, price, self.lower, self.upper):
            if self.position is not None:
                signals.append(f"🚪 EXIT {self.position} at {price}")
                self.position = None

        return signals
