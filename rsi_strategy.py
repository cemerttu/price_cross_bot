from typing import List, Dict, Any
from bot import PriceCrossBot
from indicators import rsi, get_all_indicators

class RSIStrategy:
    def __init__(self, period=14, overbought=70, oversold=30):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        self.prices: List[float] = []
        self.position = None
        self.bot = PriceCrossBot()
        self.signal_history: List[Dict] = []

    def on_price(self, price: float, prev_price: float = None) -> List[str]:
        self.prices.append(price)
        signals: List[str] = []

        if len(self.prices) < self.period:
            return signals

        current_rsi = rsi(self.prices, self.period)[-1]
        indicators = get_all_indicators(self.prices)

        if current_rsi < self.oversold and self.position != "LONG" and len(self.prices) > 20:
            self.position = "LONG"
            signal_msg = f"🟢 BUY | RSI ({current_rsi:.2f}) < Oversold ({self.oversold})"
            signals.append(signal_msg)
            self.signal_history.append(self.bot.log_trade("BUY", price, indicators))

        elif current_rsi > self.overbought and self.position != "SHORT" and len(self.prices) > 20:
            self.position = "SHORT"
            signal_msg = f"🔴 SELL | RSI ({current_rsi:.2f}) > Overbought ({self.overbought})"
            signals.append(signal_msg)
            self.signal_history.append(self.bot.log_trade("SELL", price, indicators))

        return signals

    def get_strategy_stats(self) -> Dict[str, Any]:
        return {
            "rsi_period": self.period,
            "overbought": self.overbought,
            "oversold": self.oversold,
            "current_position": self.position,
            "total_signals": len(self.signal_history),
            "data_points": len(self.prices)
        }
