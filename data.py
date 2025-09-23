import pandas as pd
import yfinance as yf
import time
from typing import Optional, Generator, Tuple, List

def load_csv_prices(file_path: str, column: str = "Close") -> Optional[List[float]]:
    try:
        df = pd.read_csv(file_path)
        if column not in df.columns:
            print(f"❌ Column '{column}' not found in CSV.")
            return None
        return [float(p) for p in df[column].dropna().tolist()]
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return None

def get_historical_data(symbol: str = "EURUSD=X", period="1d", interval="1m") -> Optional[pd.DataFrame]:
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        return df if not df.empty else None
    except Exception as e:
        print(f"❌ Error fetching historical data: {e}")
        return None

def stream_prices(symbol: str = "EURUSD=X", interval: int = 1) -> Generator[Tuple[float, float], None, None]:
    prev_price = None
    while True:
        try:
            df = yf.Ticker(symbol).history(period="1d", interval="1m")
            if not df.empty:
                price = float(df["Close"].iloc[-1])
                yield prev_price, price
                prev_price = price
        except Exception as e:
            print(f"❌ Error streaming prices: {e}")
        time.sleep(interval)
