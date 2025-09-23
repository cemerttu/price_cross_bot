from typing import List, Dict, Any

class PriceCrossBot:
    def __init__(self):
        self.trade_history = []
        self.analysis_data = []
        
    def crossing(self, price: float, level: float, tolerance: float = 0.0001) -> bool:
        """Check if price == level with tolerance for floating point precision"""
        return abs(price - level) <= tolerance

    def crossing_up(self, prev_price: float, price: float, level: float) -> bool:
        """Price crosses from below to above level"""
        return prev_price is not None and prev_price < level <= price

    def crossing_down(self, prev_price: float, price: float, level: float) -> bool:
        """Price crosses from above to below level"""
        return prev_price is not None and prev_price > level >= price

    def greater_than(self, price: float, level: float) -> bool:
        return price > level

    def less_than(self, price: float, level: float) -> bool:
        return price < level

    def inside_channel(self, price: float, lower: float, upper: float) -> bool:
        return lower <= price <= upper

    def outside_channel(self, price: float, lower: float, upper: float) -> bool:
        return price < lower or price > upper

    def entering_channel(self, prev_price: float, price: float, lower: float, upper: float) -> bool:
        """Price moves from outside into the channel"""
        if prev_price is None:
            return False
        return (prev_price < lower and lower <= price <= upper) or \
               (prev_price > upper and lower <= price <= upper)

    def exiting_channel(self, prev_price: float, price: float, lower: float, upper: float) -> bool:
        """Price moves from inside channel to outside"""
        if prev_price is None:
            return False
        return (lower <= prev_price <= upper) and \
               (price < lower or price > upper)

    def moving_up(self, prev_price: float, price: float) -> bool:
        return prev_price is not None and price > prev_price

    def moving_down(self, prev_price: float, price: float) -> bool:
        return prev_price is not None and price < prev_price

    def moving_up_percent(self, prev_price: float, price: float) -> float:
        if prev_price is None or prev_price == 0: 
            return 0
        return ((price - prev_price) / prev_price) * 100 if price > prev_price else 0

    def moving_down_percent(self, prev_price: float, price: float) -> float:
        if prev_price is None or prev_price == 0: 
            return 0
        return ((prev_price - price) / prev_price) * 100 if price < prev_price else 0

    def analyze_price_action(self, prices: List[float], window: int = 10) -> Dict[str, Any]:
        """Analyze recent price action"""
        if len(prices) < window:
            return {"error": "Insufficient data"}
        
        recent_prices = prices[-window:]
        price_changes = [recent_prices[i] - recent_prices[i-1] for i in range(1, len(recent_prices))]
        
        return {
            "current_price": recent_prices[-1],
            "price_change": recent_prices[-1] - recent_prices[0],
            "price_change_percent": ((recent_prices[-1] - recent_prices[0]) / recent_prices[0]) * 100,
            "avg_change": sum(price_changes) / len(price_changes) if price_changes else 0,
            "trend": "up" if recent_prices[-1] > recent_prices[0] else "down",
            "volatility": max(recent_prices) - min(recent_prices)
        }

    def log_trade(self, signal: str, price: float, indicator_values: Dict[str, float]):
        """Log trade signals for analysis"""
        trade_record = {
            "timestamp": self._get_timestamp(),
            "signal": signal,
            "price": price,
            "indicators": indicator_values
        }
        self.trade_history.append(trade_record)
        return trade_record

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")