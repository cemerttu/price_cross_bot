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
        return [50.0] * len(prices) if prices else []
    
    if not isinstance(prices, pd.Series):
        prices = pd.Series(prices)

    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi_series = 100 - (100 / (1 + rs))
    
    return rsi_series.fillna(50).tolist()

def stochastic_oscillator(prices: List[float], high: List[float] = None, low: List[float] = None, 
                         k_period: int = 14, d_period: int = 3) -> Dict[str, List[float]]:
    """
    Stochastic Oscillator (%K and %D)
    If high/low are not provided, uses price for all three (simplified version)
    """
    if not prices or len(prices) < k_period:
        empty_list = [0.0] * len(prices) if prices else []
        return {"%K": empty_list, "%D": empty_list}
    
    # If high/low not provided, use price (simplified calculation)
    if high is None:
        high = prices
    if low is None:
        low = prices
    
    # Ensure all lists are same length
    min_length = min(len(prices), len(high), len(low))
    prices = prices[:min_length]
    high = high[:min_length]
    low = low[:min_length]
    
    k_values = []
    for i in range(len(prices)):
        if i < k_period - 1:
            k_values.append(50.0)  # Default value
            continue
            
        current_low = min(low[i - k_period + 1:i + 1])
        current_high = max(high[i - k_period + 1:i + 1])
        
        if current_high == current_low:
            k_value = 50.0
        else:
            k_value = ((prices[i] - current_low) / (current_high - current_low)) * 100
        
        k_values.append(k_value)
    
    # Calculate %D (simple moving average of %K)
    d_values = []
    for i in range(len(k_values)):
        if i < k_period - 1 + d_period - 1:
            d_values.append(50.0)
            continue
            
        d_value = sum(k_values[i - d_period + 1:i + 1]) / d_period
        d_values.append(d_value)
    
    # Pad beginning with default values
    while len(k_values) < len(prices):
        k_values.insert(0, 50.0)
    while len(d_values) < len(prices):
        d_values.insert(0, 50.0)
    
    return {"%K": k_values, "%D": d_values}

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

def get_ema_cross_signals(prices: List[float], fast_period: int = 13, slow_period: int = 20) -> Dict[str, Any]:
    """Get EMA crossover signals specifically for EMA 13/20"""
    if len(prices) < slow_period:
        return {"signal": "no_data", "fast_ema": 0, "slow_ema": 0, "difference": 0}
    
    fast_ema_vals = ema(prices, fast_period)
    slow_ema_vals = ema(prices, slow_period)
    
    current_fast = fast_ema_vals[-1]
    current_slow = slow_ema_vals[-1]
    prev_fast = fast_ema_vals[-2] if len(fast_ema_vals) > 1 else current_fast
    prev_slow = slow_ema_vals[-2] if len(slow_ema_vals) > 1 else current_slow
    
    # Check for crossover
    golden_cross = prev_fast < prev_slow and current_fast > current_slow
    death_cross = prev_fast > prev_slow and current_fast < current_slow
    
    signal = "neutral"
    if golden_cross:
        signal = "golden_cross"
    elif death_cross:
        signal = "death_cross"
    elif current_fast > current_slow:
        signal = "bullish"
    elif current_fast < current_slow:
        signal = "bearish"
    
    return {
        "signal": signal,
        "fast_ema": current_fast,
        "slow_ema": current_slow,
        "difference": current_fast - current_slow,
        "difference_percent": ((current_fast - current_slow) / current_slow * 100) if current_slow != 0 else 0
    }

def get_all_indicators(prices: List[float]) -> Dict[str, Any]:
    """Get all technical indicators for current price analysis with focus on EMA 13/20 and Stochastic"""
    if len(prices) < 20:
        return {"error": "Insufficient data (need at least 20 periods)"}
    
    ema_cross = get_ema_cross_signals(prices, 13, 20)
    stochastic = stochastic_oscillator(prices, k_period=14, d_period=3)
    rsi_data = rsi(prices, 14)
    macd_data = macd(prices)
    
    return {
        "ema_fast_13": ema_cross["fast_ema"],
        "ema_slow_20": ema_cross["slow_ema"],
        "ema_signal": ema_cross["signal"],
        "ema_difference": ema_cross["difference"],
        "stochastic_k": stochastic["%K"][-1] if stochastic["%K"] else 50,
        "stochastic_d": stochastic["%D"][-1] if stochastic["%D"] else 50,
        "stochastic_signal": "bullish" if stochastic["%K"][-1] > stochastic["%D"][-1] else "bearish" if stochastic["%K"][-1] < stochastic["%D"][-1] else "neutral",
        "rsi": rsi_data[-1] if rsi_data else 50,
        "macd": macd_data["macd"][-1] if macd_data["macd"] else 0,
        "macd_signal": macd_data["signal"][-1] if macd_data["signal"] else 0,
        "current_price": prices[-1] if prices else 0
    }