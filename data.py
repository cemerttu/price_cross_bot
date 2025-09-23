import yfinance as yf
import time
import pandas as pd
from typing import Optional, Generator, Tuple
from datetime import datetime

def get_latest_price(symbol: str = "EURUSD=X") -> Optional[float]:
    """
    Fetch the latest close price of a symbol from Yahoo Finance with 1-second capability.
    """
    try:
        ticker = yf.Ticker(symbol)
        # Use 1m interval for higher frequency data
        df = ticker.history(period="1d", interval="1m")
        if not df.empty:
            return float(df["Close"].iloc[-1])
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
    return None

def stream_prices(symbol: str = "EURUSD=X", interval: int = 1) -> Generator[Tuple[Optional[float], float], None, None]:
    """
    Stream live prices every `interval` seconds (generator).
    Optimized for 1-second intervals.
    """
    prev_price = None
    error_count = 0
    max_errors = 5
    
    print(f"📡 Starting price stream for {symbol} at {interval}-second intervals...")
    
    while True:
        try:
            price = get_latest_price(symbol)
            if price is not None:
                yield prev_price, price
                prev_price = price
                error_count = 0  # Reset error count on success
            else:
                error_count += 1
                if error_count >= max_errors:
                    print("❌ Too many errors, stopping stream...")
                    break
                    
        except Exception as e:
            print(f"Error in price stream: {e}")
            error_count += 1
            if error_count >= max_errors:
                break
        
        time.sleep(interval)

def get_historical_data(symbol: str = "EURUSD=X", period: str = "1d", interval: str = "1m") -> Optional[pd.DataFrame]:
    """
    Get historical data for backtesting or initial analysis.
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        return df if not df.empty else None
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return None