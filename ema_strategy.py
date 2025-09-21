from indicators import ema

class EMAStrategy:
    def __init__(self, fast_period=9, slow_period=21):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.prices = []
        self.position = None

    def on_price(self, price):
        self.prices.append(price)
        signals = []

        if len(self.prices) < self.slow_period:
            return signals  # not enough data yet

        fast_ema = ema(self.prices, self.fast_period)[-1]
        slow_ema = ema(self.prices, self.slow_period)[-1]

        # --- Trading Rules ---
        if fast_ema > slow_ema and self.position != "LONG":
            self.position = "LONG"
            signals.append(f"🟢 BUY (Fast EMA {fast_ema:.5f} > Slow EMA {slow_ema:.5f})")

        elif fast_ema < slow_ema and self.position != "SHORT":
            self.position = "SHORT"
            signals.append(f"🔴 SELL (Fast EMA {fast_ema:.5f} < Slow EMA {slow_ema:.5f})")

        return signals
