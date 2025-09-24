# risk_manager.py
import csv
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Trade:
    entry_time: str
    exit_time: Optional[str]
    signal: str
    entry_price: float
    exit_price: Optional[float]
    quantity: float
    stop_loss: float
    take_profit: float
    pnl: Optional[float]
    pnl_percent: Optional[float]
    status: str  # OPEN, CLOSED, STOP_LOSS, TAKE_PROFIT

class RiskManager:
    def __init__(self, risk_per_trade: float = 0.02, stop_loss_pips: float = 0.0020, take_profit_pips: float = 0.0040):
        self.risk_per_trade = risk_per_trade  # 2% risk per trade
        self.stop_loss_pips = stop_loss_pips  # 20 pips
        self.take_profit_pips = take_profit_pips  # 40 pips (1:2 risk-reward)
        self.open_trades: List[Trade] = []
        self.closed_trades: List[Trade] = []
        self.account_balance = 10000.0  # Starting balance
        self.equity_curve = []
        
    def calculate_position_size(self, entry_price: float) -> float:
        risk_amount = self.account_balance * self.risk_per_trade
        pip_value = 10  # Standard lot pip value for EUR/USD
        position_size = risk_amount / (self.stop_loss_pips * 10000)
        return min(position_size, self.account_balance * 0.1)  # Max 10% of account
    
    def open_trade(self, signal: str, price: float) -> Trade:
        quantity = self.calculate_position_size(price)
        
        if signal == "BUY":
            stop_loss = price - self.stop_loss_pips
            take_profit = price + self.take_profit_pips
        else:  # SELL
            stop_loss = price + self.stop_loss_pips
            take_profit = price - self.take_profit_pips
            
        trade = Trade(
            entry_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            exit_time=None,
            signal=signal,
            entry_price=price,
            exit_price=None,
            quantity=quantity,
            stop_loss=stop_loss,
            take_profit=take_profit,
            pnl=None,
            pnl_percent=None,
            status="OPEN"
        )
        
        self.open_trades.append(trade)
        return trade
    
    def check_exit_conditions(self, current_price: float) -> List[Trade]:
        closed_trades = []
        
        for trade in self.open_trades[:]:
            if trade.signal == "BUY":
                if current_price <= trade.stop_loss:
                    self.close_trade(trade, current_price, "STOP_LOSS")
                    closed_trades.append(trade)
                elif current_price >= trade.take_profit:
                    self.close_trade(trade, current_price, "TAKE_PROFIT")
                    closed_trades.append(trade)
            else:  # SELL
                if current_price >= trade.stop_loss:
                    self.close_trade(trade, current_price, "STOP_LOSS")
                    closed_trades.append(trade)
                elif current_price <= trade.take_profit:
                    self.close_trade(trade, current_price, "TAKE_PROFIT")
                    closed_trades.append(trade)
                    
        return closed_trades
    
    def close_trade(self, trade: Trade, exit_price: float, reason: str):
        trade.exit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        trade.exit_price = exit_price
        trade.status = reason
        
        # Calculate PnL
        if trade.signal == "BUY":
            trade.pnl = (exit_price - trade.entry_price) * trade.quantity * 10000
        else:  # SELL
            trade.pnl = (trade.entry_price - exit_price) * trade.quantity * 10000
            
        trade.pnl_percent = (trade.pnl / (trade.entry_price * trade.quantity)) * 100
        
        # Update account balance
        self.account_balance += trade.pnl
        self.equity_curve.append(self.account_balance)
        
        self.open_trades.remove(trade)
        self.closed_trades.append(trade)
    
    def get_performance_metrics(self) -> Dict:
        if not self.closed_trades:
            return {}
            
        winning_trades = [t for t in self.closed_trades if t.pnl and t.pnl > 0]
        losing_trades = [t for t in self.closed_trades if t.pnl and t.pnl <= 0]
        
        total_pnl = sum(t.pnl for t in self.closed_trades if t.pnl)
        win_rate = len(winning_trades) / len(self.closed_trades) * 100 if self.closed_trades else 0
        
        return {
            "total_trades": len(self.closed_trades),
            "winning_trades": len(winning_trades),
            "losing_trades": len(losing_trades),
            "win_rate": win_rate,
            "total_pnl": total_pnl,
            "account_balance": self.account_balance,
            "profit_factor": abs(sum(t.pnl for t in winning_trades)) / abs(sum(t.pnl for t in losing_trades)) if losing_trades else float('inf'),
            "max_drawdown": self.calculate_max_drawdown()
        }
    
    def calculate_max_drawdown(self) -> float:
        if len(self.equity_curve) < 2:
            return 0.0
            
        peak = self.equity_curve[0]
        max_dd = 0.0
        
        for equity in self.equity_curve:
            if equity > peak:
                peak = equity
            dd = (peak - equity) / peak * 100
            if dd > max_dd:
                max_dd = dd
                
        return max_dd