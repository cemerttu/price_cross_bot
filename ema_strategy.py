from typing import List, Dict
from .bot import PriceCrossBot
from .indicators import ema, get_all_indicators

class EMAStrategy:
    def __init__(self, fast_period: int = 13, slow_period: int = 20):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.prices: List[float] = []
        self.position: str = None
        self.bot = PriceCrossBot()
        self.signal_history: List[Dict] = []

    def on_price(self, price: float) -> List[str]:
        self.prices.append(price)
        signals = []

        if len(self.prices) < self.slow_period:
            return signals

        fast_ema = ema(self.prices, self.fast_period)[-1]
        slow_ema = ema(self.prices, self.slow_period)[-1]
        indicators = get_all_indicators(self.prices)

        if fast_ema > slow_ema and self.position != "LONG":
            self.position = "LONG"
            msg = f"🟢 BUY | Fast EMA {fast_ema:.5f} > Slow EMA {slow_ema:.5f}"
            signals.append(msg)
            self.signal_history.append(
                self.bot.log_trade("BUY", price, {"fast_ema": fast_ema, "slow_ema": slow_ema, "rsi": indicators.get("rsi", 0)})
            )

        elif fast_ema < slow_ema and self.position != "SHORT":
            self.position = "SHORT"
            msg = f"🔴 SELL | Fast EMA {fast_ema:.5f} < Slow EMA {slow_ema:.5f}"
            signals.append(msg)
            self.signal_history.append(
                self.bot.log_trade("SELL", price, {"fast_ema": fast_ema, "slow_ema": slow_ema, "rsi": indicators.get("rsi", 0)})
            )

        return signals

    def get_strategy_stats(self) -> Dict:
        return {
            "fast_period": self.fast_period,
            "slow_period": self.slow_period,
            "current_position": self.position,
            "total_signals": len(self.signal_history),
            "data_points": len(self.prices)
        }
