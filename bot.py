import pandas as pd
import numpy as np

class PriceCrossBot:
    # ... (your existing methods stay the same)

    # ---------------------------
    # 🔹 Accuracy improvements
    # ---------------------------

    def ema(self, prices, period=14):
        """Exponential Moving Average"""
        return pd.Series(prices).ewm(span=period, adjust=False).mean().iloc[-1]

    def rsi(self, prices, period=14):
        """Relative Strength Index"""
        series = pd.Series(prices)
        delta = series.diff()
        gain = delta.clip(lower=0).rolling(window=period).mean()
        loss = -delta.clip(upper=0).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]

    def atr(self, highs, lows, closes, period=14):
        """Average True Range"""
        df = pd.DataFrame({"high": highs, "low": lows, "close": closes})
        df["prev_close"] = df["close"].shift(1)
        df["tr"] = df[["high", "close"]].max(axis=1) - df[["low", "close"]].min(axis=1)
        atr = df["tr"].rolling(window=period).mean()
        return atr.iloc[-1]

    def confirmed_crossing_up(self, prev_price, price, level, prices, highs, lows):
        """
        Crossing up with filters:
        - Price closes above level
        - RSI < 70 (not overbought)
        - Price > EMA
        """
        ema_val = self.ema(prices, period=14)
        rsi_val = self.rsi(prices, period=14)
        atr_val = self.atr(highs, lows, prices, period=14)

        return (
            self.crossing_up(prev_price, price, level)
            and price > ema_val
            and rsi_val < 70
            and atr_val > 0  # ensures volatility is not zero
        )

    def confirmed_crossing_down(self, prev_price, price, level, prices, highs, lows):
        """
        Crossing down with filters:
        - Price closes below level
        - RSI > 30 (not oversold)
        - Price < EMA
        """
        ema_val = self.ema(prices, period=14)
        rsi_val = self.rsi(prices, period=14)
        atr_val = self.atr(highs, lows, prices, period=14)

        return (
            self.crossing_down(prev_price, price, level)
            and price < ema_val
            and rsi_val > 30
            and atr_val > 0
        )
