from typing import List, Dict, Any
from indicators import rsi, get_all_indicators
from bot import PriceCrossBot

class RSIStrategy:
    def __init__(self, period: int = 14, overbought: int = 70, oversold: int = 30):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        self.prices = []
        self.position = None
        self.bot = PriceCrossBot()
        self.signal_history = []

    def on_price(self, price: float, prev_price: float = None) -> List[str]:
        """Process new price and return trading signals"""
        self.prices.append(price)
        signals = []

        if len(self.prices) < self.period:
            return signals  # Not enough data yet

        # Calculate RSI
        current_rsi = rsi(self.prices, self.period)[-1]
        
        # Get additional indicators for confirmation
        indicators = get_all_indicators(self.prices)
        
        # Enhanced RSI strategy with confirmation
        if (current_rsi < self.oversold and 
            self.position != "LONG" and 
            len(self.prices) > 20):  # Additional confirmation
            
            self.position = "LONG"
            signal_msg = f"🟢 BUY | RSI ({current_rsi:.2f}) < Oversold ({self.oversold})"
            signals.append(signal_msg)
            
            # Log the trade
            trade_log = self.bot.log_trade("BUY", price, {
                "rsi": current_rsi,
                "ema_12": indicators.get("ema_12", 0),
                "ema_26": indicators.get("ema_26", 0)
            })
            self.signal_history.append(trade_log)

        elif (current_rsi > self.overbought and 
              self.position != "SHORT" and 
              len(self.prices) > 20):
            
            self.position = "SHORT"
            signal_msg = f"🔴 SELL | RSI ({current_rsi:.2f}) > Overbought ({self.overbought})"
            signals.append(signal_msg)
            
            # Log the trade
            trade_log = self.bot.log_trade("SELL", price, {
                "rsi": current_rsi,
                "ema_12": indicators.get("ema_12", 0),
                "ema_26": indicators.get("ema_26", 0)
            })
            self.signal_history.append(trade_log)

        return signals

    def get_strategy_stats(self) -> Dict[str, Any]:
        """Get strategy performance statistics"""
        return {
            "rsi_period": self.period,
            "overbought": self.overbought,
            "oversold": self.oversold,
            "current_position": self.position,
            "total_signals": len(self.signal_history),
            "data_points": len(self.prices)
        }