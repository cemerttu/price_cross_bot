# risk_manager.py - FIXED VERSION
import csv
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

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
        self.pnl_file = "pnl_tracking.csv"
        
        # Initialize PnL CSV
        self._init_pnl_csv()
    
    def _init_pnl_csv(self):
        """Initialize PnL tracking CSV with headers"""
        try:
            with open(self.pnl_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    "entry_time", "exit_time", "signal", "entry_price", "exit_price", 
                    "quantity", "pnl", "pnl_percent", "status"
                ])
                writer.writeheader()
        except Exception as e:
            print(f"Error initializing PnL CSV: {e}")
    
    def _log_pnl(self, trade: Trade):
        """Log closed trade to PnL CSV"""
        try:
            with open(self.pnl_file, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    "entry_time", "exit_time", "signal", "entry_price", "exit_price", 
                    "quantity", "pnl", "pnl_percent", "status"
                ])
                
                trade_dict = {
                    "entry_time": trade.entry_time,
                    "exit_time": trade.exit_time or "",
                    "signal": trade.signal,
                    "entry_price": round(trade.entry_price, 5),
                    "exit_price": round(trade.exit_price, 5) if trade.exit_price else "",
                    "quantity": round(trade.quantity, 2),
                    "pnl": round(trade.pnl, 2) if trade.pnl else "",
                    "pnl_percent": round(trade.pnl_percent, 2) if trade.pnl_percent else "",
                    "status": trade.status
                }
                writer.writerow(trade_dict)
        except Exception as e:
            print(f"Error logging PnL: {e}")
    
    def calculate_position_size(self, entry_price: float) -> float:
        risk_amount = self.account_balance * self.risk_per_trade
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
            should_close = False
            close_reason = ""
            
            if trade.signal == "BUY":
                if current_price <= trade.stop_loss:
                    should_close = True
                    close_reason = "STOP_LOSS"
                elif current_price >= trade.take_profit:
                    should_close = True
                    close_reason = "TAKE_PROFIT"
            else:  # SELL
                if current_price >= trade.stop_loss:
                    should_close = True
                    close_reason = "STOP_LOSS"
                elif current_price <= trade.take_profit:
                    should_close = True
                    close_reason = "TAKE_PROFIT"
            
            if should_close:
                self.close_trade(trade, current_price, close_reason)
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
        
        # Log to PnL CSV
        self._log_pnl(trade)
        
        self.open_trades.remove(trade)
        self.closed_trades.append(trade)
    
    def get_performance_metrics(self) -> Dict:
        if not self.closed_trades:
            return {}
            
        winning_trades = [t for t in self.closed_trades if t.pnl and t.pnl > 0]
        losing_trades = [t for t in self.closed_trades if t.pnl and t.pnl <= 0]
        
        total_pnl = sum(t.pnl for t in self.closed_trades if t.pnl)
        win_rate = len(winning_trades) / len(self.closed_trades) * 100 if self.closed_trades else 0
        
        avg_win = sum(t.pnl for t in winning_trades) / len(winning_trades) if winning_trades else 0
        avg_loss = sum(t.pnl for t in losing_trades) / len(losing_trades) if losing_trades else 0
        
        return {
            "total_trades": len(self.closed_trades),
            "winning_trades": len(winning_trades),
            "losing_trades": len(losing_trades),
            "win_rate": round(win_rate, 2),
            "total_pnl": round(total_pnl, 2),
            "account_balance": round(self.account_balance, 2),
            "profit_factor": abs(avg_win / avg_loss) if avg_loss != 0 else float('inf'),
            "max_drawdown": round(self.calculate_max_drawdown(), 2),
            "avg_win": round(avg_win, 2),
            "avg_loss": round(avg_loss, 2)
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