from typing import List, Dict, Any
from indicators import ema, get_all_indicators
from bot import PriceCrossBot

class EMAStrategy:
    def __init__(self, fast_period: int = 9, slow_period: int = 21):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.prices = []
        self.position = None
        self.bot = PriceCrossBot()
        self.signal_history = []

    def on_price(self, price: float, prev_price: float = None) -> List[str]:
        """Process new price and return trading signals"""
        self.prices.append(price)
        signals = []

        if len(self.prices) < self.slow_period:
            return signals  # Not enough data yet

        # Calculate EMAs
        fast_ema = ema(self.prices, self.fast_period)[-1]
        slow_ema = ema(self.prices, self.slow_period)[-1]
        
        # Get additional indicators for analysis
        indicators = get_all_indicators(self.prices)
        
        # Enhanced trading logic with multiple conditions
        if (fast_ema > slow_ema and 
            self.position != "LONG" and 
            len(self.prices) > 30):  # Ensure enough data
            
            self.position = "LONG"
            signal_msg = f"🟢 BUY | Fast EMA ({fast_ema:.5f}) > Slow EMA ({slow_ema:.5f})"
            signals.append(signal_msg)
            
            # Log the trade
            trade_log = self.bot.log_trade("BUY", price, {
                "fast_ema": fast_ema,
                "slow_ema": slow_ema,
                "rsi": indicators.get("rsi", 0)
            })
            self.signal_history.append(trade_log)

        elif (fast_ema < slow_ema and 
              self.position != "SHORT" and 
              len(self.prices) > 30):
            
            self.position = "SHORT"
            signal_msg = f"🔴 SELL | Fast EMA ({fast_ema:.5f}) < Slow EMA ({slow_ema:.5f})"
            signals.append(signal_msg)
            
            # Log the trade
            trade_log = self.bot.log_trade("SELL", price, {
                "fast_ema": fast_ema,
                "slow_ema": slow_ema,
                "rsi": indicators.get("rsi", 0)
            })
            self.signal_history.append(trade_log)

        return signals

    def get_strategy_stats(self) -> Dict[str, Any]:
        """Get strategy performance statistics"""
        return {
            "fast_period": self.fast_period,
            "slow_period": self.slow_period,
            "current_position": self.position,
            "total_signals": len(self.signal_history),
            "data_points": len(self.prices)
        }