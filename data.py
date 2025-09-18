import yfinance as yf
import time

def get_latest_price(symbol="EURUSD=X"):
    """
    Fetch the latest close price of a symbol from Yahoo Finance.
    """
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="1d", interval="1m")  # last 1-minute candles
    if not df.empty:
        return df["Close"].iloc[-1]
    return None

def stream_prices(symbol="EURUSD=X", interval=5):
    """
    Stream live prices every `interval` seconds (generator).
    """
    prev_price = None
    while True:
        price = get_latest_price(symbol)
        if price:
            yield prev_price, price
            prev_price = price
        time.sleep(interval)
