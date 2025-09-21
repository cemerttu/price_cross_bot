import pandas as pd

def ema(prices, period=14):
    """Exponential Moving Average (EMA)."""
    if not isinstance(prices, pd.Series):
        prices = pd.Series(prices)
    return prices.ewm(span=period, adjust=False).mean().tolist()

def rsi(prices, period=14):
    """Relative Strength Index (RSI)."""
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
