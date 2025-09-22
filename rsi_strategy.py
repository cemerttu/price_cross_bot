from indicators import rsi, ema

class RSIStrategy:
    def __init__(self, period=14, overbought=70, oversold=30, fast_period=9, slow_period=21):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.prices = []
        self.position = None

    def on_price(self, price):
        self.prices.append(price)
        signals = []

        if len(self.prices) < max(self.period, self.slow_period):
            return signals

        last_rsi = rsi(self.prices, self.period)[-1]
        fast_ema = ema(self.prices, self.fast_period)[-1]
        slow_ema = ema(self.prices, self.slow_period)[-1]

        if last_rsi < self.oversold and fast_ema > slow_ema and self.position != "LONG":
            self.position = "LONG"
            signals.append(
                f"🟢 BUY (RSI={last_rsi:.2f} < {self.oversold}, Fast EMA={fast_ema:.5f} > Slow EMA={slow_ema:.5f})"
            )

        elif last_rsi > self.overbought and fast_ema < slow_ema and self.position != "SHORT":
            self.position = "SHORT"
            signals.append(
                f"🔴 SELL (RSI={last_rsi:.2f} > {self.overbought}, Fast EMA={fast_ema:.5f} < Slow EMA={slow_ema:.5f})"
            )

        return signals
