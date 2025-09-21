from indicators import rsi

class RSIStrategy:
    def __init__(self, period=14, overbought=70, oversold=30):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        self.prices = []
        self.position = None

    def on_price(self, price):
        self.prices.append(price)
        signals = []

        if len(self.prices) < self.period:
            return signals  # not enough data yet

        last_rsi = rsi(self.prices, self.period)[-1]

        # --- Trading Rules ---
        if last_rsi < self.oversold and self.position != "LONG":
            self.position = "LONG"
            signals.append(f"🟢 BUY (RSI {last_rsi:.2f} < {self.oversold})")

        elif last_rsi > self.overbought and self.position != "SHORT":
            self.position = "SHORT"
            signals.append(f"🔴 SELL (RSI {last_rsi:.2f} > {self.overbought})")

        return signals
