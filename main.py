from data import stream_prices
from strategy import SimpleStrategy

# Initialize strategy
strategy = SimpleStrategy(level=1.10, lower=1.09, upper=1.11)

print("🔄 Starting live trading strategy... (Ctrl+C to stop)")

# Live loop
for prev_price, price in stream_prices("EURUSD=X", interval=10):
    if prev_price is None:
        continue

    signals = strategy.on_price(prev_price, price)
    for sig in signals:
        print(sig)
