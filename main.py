from data import stream_prices
from rsi_strategy import RSIStrategy

strategy = RSIStrategy(period=14, overbought=70, oversold=30)

print("🔄 Running RSI Strategy with Yahoo Finance feed... (Ctrl+C to stop)")

for prev_price, price in stream_prices("EURUSD=X", interval=10):  # Poll every 10 sec
    if price is None:
        continue

    signals = strategy.on_price(price)
    for sig in signals:
        print(sig)
