from typing import List, Dict, Any
from indicators import rsi, get_all_indicators, get_ema_cross_signals, stochastic_oscillator
from datetime import datetime

class RSIStrategy:
    def __init__(self, period: int = 14, overbought: int = 70, oversold: int = 30):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        self.prices = []
        self.position = None
        self.entry_price = None
        self.trades = []
        self.trade_details = []

    def on_price(self, price: float, prev_price: float = None) -> List[str]:
        """Process new price and return trading signals with EMA 13/20 and Stochastic confirmation"""
        self.prices.append(price)
        signals = []

        if len(self.prices) < max(self.period, 20):  # Need enough data for all indicators
            return signals  # Not enough data yet

        # Calculate RSI
        current_rsi = rsi(self.prices, self.period)[-1]
        
        # Get EMA 13/20 context for confirmation
        ema_context = get_ema_cross_signals(self.prices, 13, 20) if len(self.prices) >= 20 else {"signal": "neutral"}
        
        # Calculate Stochastic
        stochastic = stochastic_oscillator(self.prices, k_period=14, d_period=3)
        stoch_k = stochastic["%K"][-1] if stochastic["%K"] else 50
        stoch_d = stochastic["%D"][-1] if stochastic["%D"] else 50

        # Enhanced RSI strategy with multiple confirmations
        if (current_rsi < self.oversold and 
            self.position != "LONG" and 
            ema_context.get("signal") in ["bullish", "golden_cross", "neutral"] and
            stoch_k < 30):  # Stochastic oversold confirmation
            
            close_trade_signal = ""
            if self.position == "SHORT":
                pnl = self.entry_price - price
                self.trades.append(pnl)
                trade_detail = {
                    "timestamp": datetime.now(),
                    "type": "SHORT_CLOSE",
                    "entry_price": self.entry_price,
                    "exit_price": price,
                    "pnl": pnl,
                    "rsi": current_rsi,
                    "ema_signal": ema_context.get("signal"),
                    "stoch_k": stoch_k
                }
                self.trade_details.append(trade_detail)
                close_trade_signal = f" | Closed SHORT: PnL = {pnl:.5f}"

            self.position = "LONG"
            self.entry_price = price
            signal_msg = f"🟢 BUY | RSI ({current_rsi:.1f}) < Oversold ({self.oversold}) | EMA: {ema_context.get('signal', 'N/A')} | Stoch K:{stoch_k:.1f}{close_trade_signal}"
            signals.append(signal_msg)

        elif (current_rsi > self.overbought and 
              self.position != "SHORT" and 
              ema_context.get("signal") in ["bearish", "death_cross", "neutral"] and
              stoch_k > 70):  # Stochastic overbought confirmation
            
            close_trade_signal = ""
            if self.position == "LONG":
                pnl = price - self.entry_price
                self.trades.append(pnl)
                trade_detail = {
                    "timestamp": datetime.now(),
                    "type": "LONG_CLOSE",
                    "entry_price": self.entry_price,
                    "exit_price": price,
                    "pnl": pnl,
                    "rsi": current_rsi,
                    "ema_signal": ema_context.get("signal"),
                    "stoch_k": stoch_k
                }
                self.trade_details.append(trade_detail)
                close_trade_signal = f" | Closed LONG: PnL = {pnl:.5f}"

            self.position = "SHORT"
            self.entry_price = price
            signal_msg = f"🔴 SELL | RSI ({current_rsi:.1f}) > Overbought ({self.overbought}) | EMA: {ema_context.get('signal', 'N/A')} | Stoch K:{stoch_k:.1f}{close_trade_signal}"
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
            "rsi_period": self.period,
            "overbought": self.overbought,
            "oversold": self.oversold,
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