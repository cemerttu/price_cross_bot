from data import stream_prices
from rsi_strategy import RSIStrategy

# ✅ Use your existing RSI+EMA strategy
strategy = RSIStrategy(period=14, overbought=70, oversold=30)

print("🔄 Running RSI+EMA Strategy (optimized polling)... (Ctrl+C to stop)")

# Faster polling: every 3 seconds instead of 10
for prev_price, price in stream_prices("EURUSD=X", interval=3):
    if price is None:
        continue

    # Keep strategy working exactly the same
    signals = strategy.on_price(price)
    for sig in signals:
        print(sig)
