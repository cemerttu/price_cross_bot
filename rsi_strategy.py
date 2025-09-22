from indicators import rsi, ema
from datetime import datetime

class RSIStrategy:
    def __init__(self, period=10, overbought=65, oversold=35, fast_period=5, slow_period=10):
        # Adjusted for 1-minute timeframe
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.prices = []
        self.position = None
        self.signal_count = 0

    def on_price(self, price):
        self.prices.append(price)
        signals = []

        min_data = max(self.period, self.slow_period)
        if len(self.prices) < min_data:
            print(f"📊 [{len(self.prices)}/{min_data}] Collecting 1-min data...")
            return signals

        last_rsi = rsi(self.prices, self.period)[-1]
        fast_ema = ema(self.prices, self.fast_period)[-1]
        slow_ema = ema(self.prices, self.slow_period)[-1]
        
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"📈 {current_time} - RSI({self.period}): {last_rsi:.1f}, EMA Diff: {fast_ema-slow_ema:.5f}")

        # Trading Rules optimized for 1-minute
        if last_rsi < self.oversold and fast_ema > slow_ema and self.position != "LONG":
            self.position = "LONG"
            self.signal_count += 1
            signals.append(f"🟢 BUY #{self.signal_count} (RSI {last_rsi:.1f} < {self.oversold} on 1-min)")

        elif last_rsi > self.overbought and fast_ema < slow_ema and self.position != "SHORT":
            self.position = "SHORT"
            self.signal_count += 1
            signals.append(f"🔴 SELL #{self.signal_count} (RSI {last_rsi:.1f} > {self.overbought} on 1-min)")

        return signals