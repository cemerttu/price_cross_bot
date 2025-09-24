import csv
from datetime import datetime
from typing import Dict

class PriceCrossBot:
    def __init__(self, csv_file: str = "trade_log.csv"):
        self.trade_history = []
        self.csv_file = csv_file

        # Initialize CSV with headers
        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                "timestamp", "signal", "price", "fast_ema", "slow_ema", "rsi"
            ])
            writer.writeheader()

    def log_trade(self, signal: str, price: float, indicator_values: Dict[str, float]):
        """Log trade signals for analysis and CSV"""
        trade_record = {
            "timestamp": self._get_timestamp(),
            "signal": signal,
            "price": price,
            "fast_ema": indicator_values.get("fast_ema", 0),
            "slow_ema": indicator_values.get("slow_ema", 0),
            "rsi": indicator_values.get("rsi", 0)
        }
        self.trade_history.append(trade_record)

        # Write to CSV
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=trade_record.keys())
            writer.writerow(trade_record)

        return trade_record

    def _get_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
