import pandas as pd
import numpy as np
from typing import List, Dict, Any

def ema(prices: List[float], period: int = 14) -> List[float]:
    """Exponential Moving Average (EMA)"""
    if not prices or len(prices) < period:
        return [0.0] * len(prices) if prices else []
    
    if not isinstance(prices, pd.Series):
        prices = pd.Series(prices)
    
    return prices.ewm(span=period, adjust=False).mean().tolist()

def sma(prices: List[float], period: int = 14) -> List[float]:
    """Simple Moving Average (SMA)"""
    if not prices or len(prices) < period:
        return [0.0] * len(prices) if prices else []
    
    if not isinstance(prices, pd.Series):
        prices = pd.Series(prices)
    
    return prices.rolling(window=period).mean().tolist()

def rsi(prices: List[float], period: int = 14) -> List[float]:
    """Relative Strength Index (RSI)"""
    if not prices or len(prices) <= period:
        return [50.0] * len(prices) if prices else []  # Neutral RSI
    
    if not isinstance(prices, pd.Series):
        prices = pd.Series(prices)

    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi_series = 100 - (100 / (1 + rs))
    
    return rsi_series.fillna(50).tolist()  # Fill NaN with neutral 50

def macd(prices: List[float], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Dict[str, List[float]]:
    """Moving Average Convergence Divergence (MACD)"""
    if not prices or len(prices) < slow_period:
        empty_list = [0.0] * len(prices) if prices else []
        return {"macd": empty_list, "signal": empty_list, "histogram": empty_list}
    
    ema_fast = ema(prices, fast_period)
    ema_slow = ema(prices, slow_period)
    
    macd_line = [fast - slow for fast, slow in zip(ema_fast, ema_slow)]
    signal_line = ema(macd_line, signal_period)
    
    histogram = [macd - signal for macd, signal in zip(macd_line, signal_line)]
    
    return {
        "macd": macd_line,
        "signal": signal_line,
        "histogram": histogram
    }

def bollinger_bands(prices: List[float], period: int = 20, std_dev: int = 2) -> Dict[str, List[float]]:
    """Bollinger Bands"""
    if not prices or len(prices) < period:
        empty_list = [0.0] * len(prices) if prices else []
        return {"upper": empty_list, "middle": empty_list, "lower": empty_list}
    
    if not isinstance(prices, pd.Series):
        prices = pd.Series(prices)
    
    middle_band = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    
    upper_band = middle_band + (std * std_dev)
    lower_band = middle_band - (std * std_dev)
    
    return {
        "upper": upper_band.tolist(),
        "middle": middle_band.tolist(),
        "lower": lower_band.tolist()
    }

def get_all_indicators(prices: List[float]) -> Dict[str, Any]:
    """Get all technical indicators for current price analysis"""
    if len(prices) < 26:  # MACD requires 26 periods
        return {}
    
    return {
        "sma_20": sma(prices, 20)[-1],
        "ema_12": ema(prices, 12)[-1],
        "ema_26": ema(prices, 26)[-1],
        "rsi": rsi(prices, 14)[-1],
        "macd": macd(prices)["macd"][-1],
        "macd_signal": macd(prices)["signal"][-1]
    }