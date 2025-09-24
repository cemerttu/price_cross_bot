# backtester.py
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
from enhanced_strategy import EnhancedStrategy
from risk_manager import RiskManager

class Backtester:
    def __init__(self, initial_balance: float = 10000.0):
        self.initial_balance = initial_balance
        self.results = {}
        
    def run_backtest(self, historical_data: pd.DataFrame, strategy_params: Dict = None) -> Dict[str, Any]:
        if strategy_params is None:
            strategy_params = {}
            
        strategy = EnhancedStrategy(**strategy_params)
        strategy.risk_manager.account_balance = self.initial_balance
        
        prices = historical_data['Close'].tolist()
        timestamps = historical_data.index.tolist()
        
        trades = []
        equity_curve = [self.initial_balance]
        
        for i, price in enumerate(prices):
            # Run strategy
            signals = strategy.on_price(price)
            
            # Record equity
            current_equity = strategy.risk_manager.account_balance
            if strategy.risk_manager.open_trades:
                # Include unrealized PnL
                for trade in strategy.risk_manager.open_trades:
                    if trade.signal == "BUY":
                        unrealized = (price - trade.entry_price) * trade.quantity * 10000
                    else:
                        unrealized = (trade.entry_price - price) * trade.quantity * 10000
                    current_equity += unrealized
                    
            equity_curve.append(current_equity)
            
            # Record trade if signal generated
            if signals and "BUY" in signals[0] or "SELL" in signals[0]:
                trades.append({
                    'timestamp': timestamps[i] if i < len(timestamps) else datetime.now(),
                    'price': price,
                    'signal': 'BUY' if 'BUY' in signals[0] else 'SELL',
                    'equity': current_equity
                })
        
        # Calculate metrics
        perf_metrics = strategy.get_strategy_stats()
        perf_metrics['final_balance'] = strategy.risk_manager.account_balance
        perf_metrics['total_return'] = ((strategy.risk_manager.account_balance - self.initial_balance) / self.initial_balance) * 100
        perf_metrics['equity_curve'] = equity_curve
        perf_metrics['trades'] = trades
        
        self.results = perf_metrics
        return perf_metrics
    
    def generate_report(self) -> str:
        if not self.results:
            return "No backtest results available."
            
        report = f"""
📊 BACKTESTING REPORT
{'='*50}
Initial Balance: ${self.initial_balance:,.2f}
Final Balance: ${self.results.get('final_balance', 0):,.2f}
Total Return: {self.results.get('total_return', 0):.2f}%

📈 PERFORMANCE METRICS
Total Trades: {self.results.get('total_trades', 0)}
Winning Trades: {self.results.get('winning_trades', 0)}
Losing Trades: {self.results.get('losing_trades', 0)}
Win Rate: {self.results.get('win_rate', 0):.1f}%
Profit Factor: {self.results.get('profit_factor', 0):.2f}
Max Drawdown: {self.results.get('max_drawdown', 0):.2f}%

⚙️ STRATEGY PARAMETERS
EMA Fast Period: {self.results.get('fast_period', 0)}
EMA Slow Period: {self.results.get('slow_period', 0)}
RSI Period: {self.results.get('rsi_period', 0)}
        """
        
        return report