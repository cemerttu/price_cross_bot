# enhanced_strategy.py
from typing import List, Dict, Any
from bot import PriceCrossBot
from indicators import ema, rsi, get_all_indicators
from risk_manager import RiskManager

class EnhancedStrategy:
    def __init__(self, fast_period: int = 13, slow_period: int = 20, rsi_period: int = 14):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.rsi_period = rsi_period
        self.prices: List[float] = []
        self.position: str = None
        self.bot = PriceCrossBot()
        self.risk_manager = RiskManager()
        self.signal_history: List[Dict] = []

    def on_price(self, price: float) -> List[str]:
        self.prices.append(price)
        signals = []

        # Check exit conditions first
        closed_trades = self.risk_manager.check_exit_conditions(price)
        for trade in closed_trades:
            signals.append(f"🔒 CLOSED {trade.signal} | PnL: ${trade.pnl:.2f} ({trade.pnl_percent:.2f}%) | {trade.status}")

        if len(self.prices) < max(self.slow_period, self.rsi_period):
            return signals

        # Get all indicators
        fast_ema = ema(self.prices, self.fast_period)[-1]
        slow_ema = ema(self.prices, self.slow_period)[-1]
        current_rsi = rsi(self.prices, self.rsi_period)[-1]
        indicators = get_all_indicators(self.prices)

        # Combined strategy logic
        ema_bullish = fast_ema > slow_ema
        ema_bearish = fast_ema < slow_ema
        rsi_oversold = current_rsi < 30
        rsi_overbought = current_rsi > 70
        rsi_neutral = 30 <= current_rsi <= 70

        # ENTRY SIGNALS with confirmation
        if (ema_bullish and rsi_oversold) and self.position != "LONG":
            # Strong buy signal: EMA bullish + RSI oversold (reversal)
            self.position = "LONG"
            trade = self.risk_manager.open_trade("BUY", price)
            msg = f"🟢 STRONG BUY | EMA Bullish + RSI Oversold ({current_rsi:.1f})"
            signals.append(msg)
            self.signal_history.append(
                self.bot.log_trade("BUY", price, {
                    "fast_ema": fast_ema, 
                    "slow_ema": slow_ema, 
                    "rsi": current_rsi,
                    "stop_loss": trade.stop_loss,
                    "take_profit": trade.take_profit
                })
            )

        elif (ema_bearish and rsi_overbought) and self.position != "SHORT":
            # Strong sell signal: EMA bearish + RSI overbought (reversal)
            self.position = "SHORT"
            trade = self.risk_manager.open_trade("SELL", price)
            msg = f"🔴 STRONG SELL | EMA Bearish + RSI Overbought ({current_rsi:.1f})"
            signals.append(msg)
            self.signal_history.append(
                self.bot.log_trade("SELL", price, {
                    "fast_ema": fast_ema, 
                    "slow_ema": slow_ema, 
                    "rsi": current_rsi,
                    "stop_loss": trade.stop_loss,
                    "take_profit": trade.take_profit
                })
            )

        elif (ema_bullish and rsi_neutral) and self.position != "LONG":
            # Moderate buy signal: EMA bullish + RSI neutral (trend following)
            self.position = "LONG"
            trade = self.risk_manager.open_trade("BUY", price)
            msg = f"🟡 MODERATE BUY | EMA Bullish + RSI Neutral ({current_rsi:.1f})"
            signals.append(msg)
            self.signal_history.append(
                self.bot.log_trade("BUY", price, {
                    "fast_ema": fast_ema, 
                    "slow_ema": slow_ema, 
                    "rsi": current_rsi,
                    "stop_loss": trade.stop_loss,
                    "take_profit": trade.take_profit
                })
            )

        elif (ema_bearish and rsi_neutral) and self.position != "SHORT":
            # Moderate sell signal: EMA bearish + RSI neutral (trend following)
            self.position = "SHORT"
            trade = self.risk_manager.open_trade("SELL", price)
            msg = f"🟡 MODERATE SELL | EMA Bearish + RSI Neutral ({current_rsi:.1f})"
            signals.append(msg)
            self.signal_history.append(
                self.bot.log_trade("SELL", price, {
                    "fast_ema": fast_ema, 
                    "slow_ema": slow_ema, 
                    "rsi": current_rsi,
                    "stop_loss": trade.stop_loss,
                    "take_profit": trade.take_profit
                })
            )

        return signals

    def get_strategy_stats(self) -> Dict[str, Any]:
        base_stats = {
            "fast_period": self.fast_period,
            "slow_period": self.slow_period,
            "rsi_period": self.rsi_period,
            "current_position": self.position,
            "total_signals": len(self.signal_history),
            "data_points": len(self.prices),
            "open_trades": len(self.risk_manager.open_trades)
        }
        
        # Add performance metrics
        perf_metrics = self.risk_manager.get_performance_metrics()
        base_stats.update(perf_metrics)
        
        return base_stats