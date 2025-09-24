# bot.py - ENHANCED
import csv
from datetime import datetime
from typing import Dict
import os

class PriceCrossBot:
    def __init__(self, csv_file: str = "trade_log.csv"):
        self.trade_history = []
        self.csv_file = csv_file
        self.pnl_file = "pnl_tracking.csv"

        # Initialize CSV with headers
        for file, headers in [(self.csv_file, ["timestamp", "signal", "price", "fast_ema", "slow_ema", "rsi", "stop_loss", "take_profit"]),
                              (self.pnl_file, ["entry_time", "exit_time", "signal", "entry_price", "exit_price", "quantity", "pnl", "pnl_percent", "status"])]:
            if not os.path.exists(file):
                with open(file, mode='w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()

    def log_trade(self, signal: str, price: float, indicator_values: Dict[str, float]):
        """Log trade signals for analysis and CSV"""
        trade_record = {
            "timestamp": self._get_timestamp(),
            "signal": signal,
            "price": price,
            "fast_ema": indicator_values.get("fast_ema", 0),
            "slow_ema": indicator_values.get("slow_ema", 0),
            "rsi": indicator_values.get("rsi", 0),
            "stop_loss": indicator_values.get("stop_loss", 0),
            "take_profit": indicator_values.get("take_profit", 0)
        }
        self.trade_history.append(trade_record)

        # Write to CSV
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=trade_record.keys())
            writer.writerow(trade_record)

        return trade_record

    def log_pnl(self, trade_data: Dict):
        """Log PnL data for closed trades"""
        with open(self.pnl_file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=trade_data.keys())
            writer.writerow(trade_data)

    def _get_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")