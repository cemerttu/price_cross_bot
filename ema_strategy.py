from indicators import ema
from datetime import datetime

class EMAStrategy:
    def __init__(self, fast_period=5, slow_period=10):  # Shorter periods for 1-min
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.prices = []
        self.position = None
        self.signal_count = 0

    def on_price(self, price):
        self.prices.append(price)
        signals = []

        if len(self.prices) < self.slow_period:
            print(f"📊 [{len(self.prices)}/{self.slow_period}] Collecting 1-min data...")
            return signals

        fast_ema = ema(self.prices, self.fast_period)[-1]
        slow_ema = ema(self.prices, self.slow_period)[-1]
        
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"📈 {current_time} - EMA({self.fast_period}): {fast_ema:.5f}, EMA({self.slow_period}): {slow_ema:.5f}")

        # Trading Rules for 1-minute timeframe
        if fast_ema > slow_ema and self.position != "LONG":
            self.position = "LONG"
            self.signal_count += 1
            signals.append(f"🟢 BUY #{self.signal_count} (Fast EMA > Slow EMA on 1-min TF)")

        elif fast_ema < slow_ema and self.position != "SHORT":
            self.position = "SHORT"
            self.signal_count += 1
            signals.append(f"🔴 SELL #{self.signal_count} (Fast EMA < Slow EMA on 1-min TF)")

        return signals