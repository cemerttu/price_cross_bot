import yfinance as yf
import time
from datetime import datetime

def get_latest_price(symbol="EURUSD=X"):
    """Fetch the latest close price from Yahoo Finance with 1-minute data."""
    try:
        ticker = yf.Ticker(symbol)
        # Get 1-minute interval data for the current day
        df = ticker.history(period="1d", interval="1m")
        if not df.empty:
            return df["Close"].iloc[-1]
        return None
    except Exception as e:
        print(f"❌ Error fetching price: {e}")
        return None

def stream_prices(symbol="EURUSD=X", interval=60):  # 60 seconds = 1 minute
    """Stream live prices every `interval` seconds (now 1 minute)."""
    prev_price = None
    print(f"📡 Streaming {symbol} every {interval//60} minute(s)...")
    
    while True:
        price = get_latest_price(symbol)
        if price:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"⏰ {current_time} - New price: {price:.5f}")
            yield prev_price, price
            prev_price = price
        time.sleep(interval)