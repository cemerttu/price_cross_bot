from bot import PriceCrossBot
from indicators import ema, rsi

class AdvancedStrategy:
    def __init__(self, level=1.10, lower=1.09, upper=1.11, ema_period=20, rsi_period=14):
        self.bot = PriceCrossBot()
        self.level = level
        self.lower = lower
        self.upper = upper
        self.ema_period = ema_period
        self.rsi_period = rsi_period
        self.position = None
        self.prices = []

    def on_price(self, prev_price, price):
        self.prices.append(price)
        signals = []

        # --- Indicators ---
        ema_values = ema(self.prices, self.ema_period)
        rsi_values = rsi(self.prices, self.rsi_period)

        last_ema = ema_values[-1] if ema_values else None
        last_rsi = rsi_values[-1] if rsi_values else None

        # --- Trading rules ---
        if last_ema and last_rsi:
            if price > last_ema and last_rsi < 70:
                if self.position != "LONG":
                    self.position = "LONG"
                    signals.append(f"🟢 BUY (EMA={last_ema:.5f}, RSI={last_rsi:.2f})")

            elif price < last_ema and last_rsi > 30:
                if self.position != "SHORT":
                    self.position = "SHORT"
                    signals.append(f"🔴 SELL (EMA={last_ema:.5f}, RSI={last_rsi:.2f})")

        return signals
