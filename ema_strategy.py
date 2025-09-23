from typing import List, Dict, Any
from indicators import ema, get_all_indicators, stochastic_oscillator
from datetime import datetime

class EMAStrategy:
    def __init__(self, fast_period: int = 13, slow_period: int = 20):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.prices = []
        self.position = None
        self.entry_price = None
        self.trades = []  # Store trade history
        self.trade_details = []  # Store detailed trade info

    def on_price(self, price: float, prev_price: float = None) -> List[str]:
        """Process new price and return trading signals with Stochastic confirmation"""
        self.prices.append(price)
        signals = []

        if len(self.prices) < self.slow_period:
            return signals  # Not enough data yet

        # Calculate EMAs
        fast_ema = ema(self.prices, self.fast_period)[-1]
        slow_ema = ema(self.prices, self.slow_period)[-1]
        
        # Calculate Stochastic
        stochastic = stochastic_oscillator(self.prices, k_period=14, d_period=3)
        stoch_k = stochastic["%K"][-1] if stochastic["%K"] else 50
        stoch_d = stochastic["%D"][-1] if stochastic["%D"] else 50
        
        # Stochastic signals
        stoch_bullish = stoch_k > stoch_d and stoch_k < 80  # K above D but not overbought
        stoch_bearish = stoch_k < stoch_d and stoch_k > 20  # K below D but not oversold
        stoch_overbought = stoch_k > 80
        stoch_oversold = stoch_k < 20

        # === BUY SIGNAL === (EMA bullish + Stochastic confirmation)
        if (fast_ema > slow_ema and 
            self.position != "LONG" and 
            (stoch_bullish or stoch_oversold)):  # Stochastic confirmation
            
            close_trade_signal = ""
            if self.position == "SHORT":  
                # Close short trade before opening long
                pnl = self.entry_price - price
                self.trades.append(pnl)
                trade_detail = {
                    "timestamp": datetime.now(),
                    "type": "SHORT_CLOSE",
                    "entry_price": self.entry_price,
                    "exit_price": price,
                    "pnl": pnl,
                    "ema_fast": fast_ema,
                    "ema_slow": slow_ema,
                    "stoch_k": stoch_k,
                    "stoch_d": stoch_d
                }
                self.trade_details.append(trade_detail)
                close_trade_signal = f" | Closed SHORT: PnL = {pnl:.5f}"

            self.position = "LONG"
            self.entry_price = price
            stoch_status = "Oversold" if stoch_oversold else "Bullish"
            signal_msg = f"🟢 BUY | EMA{self.fast_period}({fast_ema:.5f}) > EMA{self.slow_period}({slow_ema:.5f}) | Stoch {stoch_status} (K:{stoch_k:.1f}/D:{stoch_d:.1f}){close_trade_signal}"
            signals.append(signal_msg)

        # === SELL SIGNAL === (EMA bearish + Stochastic confirmation)
        elif (fast_ema < slow_ema and 
              self.position != "SHORT" and 
              (stoch_bearish or stoch_overbought)):  # Stochastic confirmation
            
            close_trade_signal = ""
            if self.position == "LONG":
                # Close long trade before opening short
                pnl = price - self.entry_price
                self.trades.append(pnl)
                trade_detail = {
                    "timestamp": datetime.now(),
                    "type": "LONG_CLOSE", 
                    "entry_price": self.entry_price,
                    "exit_price": price,
                    "pnl": pnl,
                    "ema_fast": fast_ema,
                    "ema_slow": slow_ema,
                    "stoch_k": stoch_k,
                    "stoch_d": stoch_d
                }
                self.trade_details.append(trade_detail)
                close_trade_signal = f" | Closed LONG: PnL = {pnl:.5f}"

            self.position = "SHORT"
            self.entry_price = price
            stoch_status = "Overbought" if stoch_overbought else "Bearish"
            signal_msg = f"🔴 SELL | EMA{self.fast_period}({fast_ema:.5f}) < EMA{self.slow_period}({slow_ema:.5f}) | Stoch {stoch_status} (K:{stoch_k:.1f}/D:{stoch_d:.1f}){close_trade_signal}"
            signals.append(signal_msg)

        return signals

    def get_strategy_stats(self) -> Dict[str, Any]:
        """Get strategy performance statistics"""
        wins = len([t for t in self.trades if t > 0])
        losses = len([t for t in self.trades if t <= 0])
        total = len(self.trades)
        win_rate = (wins / total * 100) if total > 0 else 0
        profit = sum(self.trades)
        
        # Calculate max drawdown
        running_profit = 0
        peak = 0
        max_drawdown = 0
        for trade in self.trades:
            running_profit += trade
            if running_profit > peak:
                peak = running_profit
            drawdown = peak - running_profit
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        return {
            "fast_period": self.fast_period,
            "slow_period": self.slow_period,
            "current_position": self.position,
            "open_entry_price": self.entry_price,
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": f"{win_rate:.2f}%",
            "net_profit": profit,
            "max_drawdown": max_drawdown,
            "data_points": len(self.prices),
            "trade_details": self.trade_details
        }

    def get_current_indicators(self) -> Dict[str, Any]:
        """Get current indicator values"""
        if len(self.prices) < self.slow_period:
            return {}
        
        indicators = get_all_indicators(self.prices)
        return indicators