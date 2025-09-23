from typing import List, Dict, Any
from bot import PriceCrossBot
from indicators import ema, get_all_indicators

class EMAStrategy:
    def __init__(self, fast_period=9, slow_period=21):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.prices: List[float] = []
        self.position = None
        self.bot = PriceCrossBot()
        self.signal_history: List[Dict] = []

    def on_price(self, price: float, prev_price: float = None) -> List[str]:
        self.prices.append(price)
        signals: List[str] = []

        if len(self.prices) < self.slow_period:
            return signals

        fast_ema = ema(self.prices, self.fast_period)[-1]
        slow_ema = ema(self.prices, self.slow_period)[-1]
        indicators = get_all_indicators(self.prices)

        if fast_ema > slow_ema and self.position != "LONG" and len(self.prices) > 30:
            self.position = "LONG"
            signal_msg = f"🟢 BUY | Fast EMA ({fast_ema:.5f}) > Slow EMA ({slow_ema:.5f})"
            signals.append(signal_msg)
            self.signal_history.append(self.bot.log_trade("BUY", price, indicators))

        elif fast_ema < slow_ema and self.position != "SHORT" and len(self.prices) > 30:
            self.position = "SHORT"
            signal_msg = f"🔴 SELL | Fast EMA ({fast_ema:.5f}) < Slow EMA ({slow_ema:.5f})"
            signals.append(signal_msg)
            self.signal_history.append(self.bot.log_trade("SELL", price, indicators))

        return signals

    def get_strategy_stats(self) -> Dict[str, Any]:
        return {
            "fast_period": self.fast_period,
            "slow_period": self.slow_period,
            "current_position": self.position,
            "total_signals": len(self.signal_history),
            "data_points": len(self.prices)
        }
