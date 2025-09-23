import yfinance as yf
import time
from typing import Generator, Tuple, Optional
import pandas as pd

def get_latest_price(symbol: str = "EURUSD=X") -> Optional[float]:
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1d", interval="1m")
        if not df.empty:
            return float(df["Close"].iloc[-1])
    except Exception as e:
        print(f"Error fetching price: {e}")
    return None

def stream_prices(symbol: str = "EURUSD=X", interval: int = 1) -> Generator[Tuple[Optional[float], float], None, None]:
    prev_price = None
    while True:
        price = get_latest_price(symbol)
        if price is not None:
            yield prev_price, price
            prev_price = price
        time.sleep(interval)

def get_historical_data(symbol: str = "EURUSD=X", period: str = "1d", interval: str = "1m") -> pd.DataFrame:
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        return df
    except:
        return pd.DataFrame()
