import pandas as pd
from typing import List, Dict

def ema(prices: List[float], period: int = 14) -> List[float]:
    if not prices or len(prices) < period:
        return [0.0] * len(prices) if prices else []
    prices = pd.Series(prices)
    return prices.ewm(span=period, adjust=False).mean().tolist()

def sma(prices: List[float], period: int = 14) -> List[float]:
    prices = pd.Series(prices)
    return prices.rolling(window=period).mean().tolist()

def rsi(prices: List[float], period: int = 14) -> List[float]:
    prices = pd.Series(prices)
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi_series = 100 - (100 / (1 + rs))
    return rsi_series.fillna(50).tolist()

def get_all_indicators(prices: List[float]) -> Dict[str, float]:
    if len(prices) < 26:
        return {}
    return {
        "ema_12": ema(prices, 12)[-1],
        "ema_26": ema(prices, 26)[-1],
        "sma_20": sma(prices, 20)[-1],
        "rsi": rsi(prices, 14)[-1]
    }
