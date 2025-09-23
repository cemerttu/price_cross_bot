from typing import List, Dict, Any
from datetime import datetime

class PriceCrossBot:
    def __init__(self):
        self.trade_history = []

    def log_trade(self, signal: str, price: float, indicator_values: Dict[str, float]):
        trade_record = {
            "timestamp": self._get_timestamp(),
            "signal": signal,
            "price": price,
            "indicators": indicator_values
        }
        self.trade_history.append(trade_record)
        return trade_record

    def _get_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
