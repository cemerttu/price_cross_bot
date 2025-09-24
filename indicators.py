# indicators.py - FIXED RSI CALCULATION
import pandas as pd
import numpy as np
from typing import List, Dict

def ema(prices: List[float], period: int = 14) -> List[float]:
    if not prices or len(prices) < period:
        return [0.0] * len(prices) if prices else []
    prices = pd.Series(prices)
    return prices.ewm(span=period, adjust=False).mean().tolist()

def sma(prices: List[float], period: int = 14) -> List[float]:
    if len(prices) < period:
        return [0.0] * len(prices)
    prices = pd.Series(prices)
    return prices.rolling(window=period).mean().tolist()

def rsi(prices: List[float], period: int = 14) -> List[float]:
    if len(prices) < period + 1:
        return [50.0] * len(prices)  # Default to neutral RSI
    
    prices_series = pd.Series(prices)
    delta = prices_series.diff()
    
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi_series = 100 - (100 / (1 + rs))
    
    # Fill NaN values with 50 (neutral)
    return rsi_series.fillna(50).tolist()

def get_all_indicators(prices: List[float]) -> Dict[str, float]:
    if len(prices) < 26:
        return {"ema_12": 0, "ema_26": 0, "sma_20": 0, "rsi": 50}
    
    return {
        "ema_12": ema(prices, 12)[-1],
        "ema_26": ema(prices, 26)[-1],
        "sma_20": sma(prices, 20)[-1],
        "rsi": rsi(prices, 14)[-1]
    }